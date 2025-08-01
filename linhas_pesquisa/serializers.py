from rest_framework import serializers
from .models import LinhaPesquisa, Pesquisador, Estudante, ConfiguracaoPagina


class PesquisadorSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Pesquisador"""
    
    class Meta:
        model = Pesquisador
        fields = ['id', 'nome', 'universidade', 'link_lattes', 'ativo']
        read_only_fields = ['id']
    
    def to_representation(self, instance):
        """Customizar a representação dos dados"""
        data = super().to_representation(instance)
        
        # Adicionar informações extras se necessário
        data['display_name'] = f"{instance.nome} ({instance.universidade})"
        data['has_lattes'] = bool(instance.link_lattes)
        
        return data


class EstudanteSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Estudante"""
    nivel_display = serializers.CharField(source='get_nivel_display', read_only=True)
    
    class Meta:
        model = Estudante
        fields = [
            'id', 'nome', 'nivel', 'nivel_display', 
            'universidade', 'programa', 'link_lattes', 'ativo'
        ]
        read_only_fields = ['id', 'nivel_display']
    
    def to_representation(self, instance):
        """Customizar a representação dos dados"""
        data = super().to_representation(instance)
        
        # Adicionar informações extras
        data['display_name'] = f"{instance.nome} - {instance.get_nivel_display()}"
        data['instituicao_completa'] = f"{instance.universidade}"
        if instance.programa:
            data['instituicao_completa'] += f"/{instance.programa}"
        data['has_lattes'] = bool(instance.link_lattes)
        
        return data


class LinhaPesquisaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo LinhaPesquisa"""
    pesquisadores = PesquisadorSerializer(many=True, read_only=True)
    estudantes = EstudanteSerializer(many=True, read_only=True)
    palavras_chave_list = serializers.SerializerMethodField()
    total_pesquisadores = serializers.SerializerMethodField()
    total_estudantes = serializers.SerializerMethodField()
    coordenador = serializers.SerializerMethodField()
    estudantes_por_nivel = serializers.SerializerMethodField()
    
    class Meta:
        model = LinhaPesquisa
        fields = [
            'id', 'titulo', 'objetivo', 'palavras_chave', 'palavras_chave_list',
            'setores_aplicacao', 'imagem', 'pesquisadores', 'estudantes',
            'ativa', 'ordem', 'data_criacao', 'data_atualizacao',
            'total_pesquisadores', 'total_estudantes', 'coordenador',
            'estudantes_por_nivel'
        ]
        read_only_fields = ['id', 'data_criacao', 'data_atualizacao']
    
    def get_palavras_chave_list(self, obj):
        """Retorna lista de palavras-chave"""
        return obj.get_palavras_chave_list()
    
    def get_total_pesquisadores(self, obj):
        """Retorna total de pesquisadores ativos"""
        return obj.pesquisadores.filter(ativo=True).count()
    
    def get_total_estudantes(self, obj):
        """Retorna total de estudantes ativos"""
        return obj.estudantes.filter(ativo=True).count()
    
    def get_coordenador(self, obj):
        """Retorna o coordenador da linha de pesquisa"""
        coordenador = obj.get_pesquisadores_coordenadores()
        if coordenador:
            return PesquisadorSerializer(coordenador).data
        return None
    
    def get_estudantes_por_nivel(self, obj):
        """Retorna estudantes agrupados por nível"""
        estudantes_dict = obj.get_estudantes_por_nivel()
        
        # Converter para formato adequado para JSON
        resultado = {}
        for nivel, estudantes in estudantes_dict.items():
            resultado[nivel] = EstudanteSerializer(estudantes, many=True).data
        
        return resultado
    
    def to_representation(self, instance):
        """Customizar a representação dos dados"""
        data = super().to_representation(instance)
        
        # Adicionar URL da imagem se existir
        if instance.imagem:
            request = self.context.get('request')
            if request:
                data['imagem_url'] = request.build_absolute_uri(instance.imagem.url)
            else:
                data['imagem_url'] = instance.imagem.url
        else:
            data['imagem_url'] = None
        
        # Adicionar informações de resumo
        data['resumo'] = {
            'total_pessoas': data['total_pesquisadores'] + data['total_estudantes'],
            'tem_imagem': bool(instance.imagem),
            'tem_coordenador': bool(data['coordenador']),
            'niveis_estudantes': list(data['estudantes_por_nivel'].keys()) if data['estudantes_por_nivel'] else []
        }
        
        return data


class ConfiguracaoPaginaSerializer(serializers.ModelSerializer):
    """Serializer para configurações da página"""
    
    class Meta:
        model = ConfiguracaoPagina
        fields = ['titulo_pagina', 'descricao_pagina', 'imagem_hero']
    
    def to_representation(self, instance):
        """Customizar a representação dos dados"""
        data = super().to_representation(instance)
        
        # Adicionar URL da imagem hero se existir
        if instance.imagem_hero:
            request = self.context.get('request')
            if request:
                data['imagem_hero_url'] = request.build_absolute_uri(instance.imagem_hero.url)
            else:
                data['imagem_hero_url'] = instance.imagem_hero.url
        else:
            data['imagem_hero_url'] = None
        
        return data


class EstatisticasSerializer(serializers.Serializer):
    """Serializer para estatísticas gerais"""
    total_linhas = serializers.IntegerField()
    total_pesquisadores = serializers.IntegerField()
    total_estudantes = serializers.IntegerField()
    linhas_mais_populares = serializers.ListField(child=serializers.DictField())
    distribuicao_estudantes = serializers.DictField()
    universidades_participantes = serializers.ListField(child=serializers.CharField())
    
    def to_representation(self, instance):
        """Customizar a representação dos dados"""
        data = super().to_representation(instance)
        
        # Adicionar informações calculadas
        if data['total_linhas'] > 0:
            data['media_pesquisadores_por_linha'] = round(
                data['total_pesquisadores'] / data['total_linhas'], 2
            )
            data['media_estudantes_por_linha'] = round(
                data['total_estudantes'] / data['total_linhas'], 2
            )
        else:
            data['media_pesquisadores_por_linha'] = 0
            data['media_estudantes_por_linha'] = 0
        
        return data


# Serializers para formulários (se necessário)
class LinhaPesquisaCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de linhas de pesquisa"""
    
    class Meta:
        model = LinhaPesquisa
        fields = [
            'titulo', 'objetivo', 'palavras_chave', 'setores_aplicacao',
            'imagem', 'pesquisadores', 'estudantes', 'ordem'
        ]
    
    def validate_titulo(self, value):
        """Validar título único"""
        if LinhaPesquisa.objects.filter(titulo=value).exists():
            raise serializers.ValidationError("Já existe uma linha de pesquisa com este título.")
        return value
    
    def validate_palavras_chave(self, value):
        """Validar formato das palavras-chave"""
        if not value:
            raise serializers.ValidationError("Palavras-chave são obrigatórias.")
        
        palavras = [p.strip() for p in value.split(';') if p.strip()]
        if len(palavras) < 2:
            raise serializers.ValidationError("Informe pelo menos 2 palavras-chave separadas por ponto e vírgula.")
        
        return value


class PesquisadorCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de pesquisadores"""
    
    class Meta:
        model = Pesquisador
        fields = ['nome', 'universidade', 'link_lattes']
    
    def validate_nome(self, value):
        """Validar nome único"""
        if Pesquisador.objects.filter(nome=value).exists():
            raise serializers.ValidationError("Já existe um pesquisador com este nome.")
        return value


class EstudanteCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de estudantes"""
    
    class Meta:
        model = Estudante
        fields = ['nome', 'nivel', 'universidade', 'programa', 'link_lattes']
    
    def validate(self, data):
        """Validações customizadas"""
        # Verificar se nome + universidade + nível é único
        if Estudante.objects.filter(
            nome=data['nome'],
            universidade=data['universidade'],
            nivel=data['nivel']
        ).exists():
            raise serializers.ValidationError(
                "Já existe um estudante com este nome, universidade e nível."
            )
        
        return data

