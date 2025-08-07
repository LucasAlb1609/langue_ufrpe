from rest_framework import serializers
from .models import PublicacaoPDF, Organizador, ConfiguracaoPaginaPublicacoes


class OrganizadorSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Organizador"""
    
    total_publicacoes = serializers.SerializerMethodField()
    
    class Meta:
        model = Organizador
        fields = [
            'id',
            'nome',
            'biografia',
            'lattes_link',
            'email',
            'total_publicacoes',
            'criado_em',
            'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
    
    def get_total_publicacoes(self, obj):
        """Retorna o total de publicações ativas do organizador"""
        return obj.publicacoes.filter(ativa=True).count()


class OrganizadorSimplificadoSerializer(serializers.ModelSerializer):
    """Serializer simplificado para organizador (para uso em PublicacaoPDFSerializer)"""
    
    class Meta:
        model = Organizador
        fields = ['id', 'nome', 'lattes_link']


class PublicacaoPDFSerializer(serializers.ModelSerializer):
    """Serializer para o modelo PublicacaoPDF"""
    
    organizadores = OrganizadorSimplificadoSerializer(many=True, read_only=True)
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    titulo_completo = serializers.CharField(read_only=True)
    organizadores_display = serializers.CharField(source='get_organizadores_display', read_only=True)
    tamanho_arquivo_mb = serializers.FloatField(read_only=True)
    arquivo_pdf_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PublicacaoPDF
        fields = [
            'id',
            'titulo',
            'subtitulo',
            'titulo_completo',
            'organizadores',
            'organizadores_display',
            'categoria',
            'categoria_display',
            'descricao',
            'ano_publicacao',
            'editora',
            'isbn',
            'numero_paginas',
            'arquivo_pdf_url',
            'thumbnail_url',
            'destaque',
            'downloads',
            'tamanho_arquivo_mb',
            'criado_em',
            'atualizado_em'
        ]
        read_only_fields = [
            'id',
            'downloads',
            'criado_em',
            'atualizado_em'
        ]
    
    def get_arquivo_pdf_url(self, obj):
        """Retorna URL completa do arquivo PDF"""
        if obj.arquivo_pdf:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.arquivo_pdf.url)
            return obj.arquivo_pdf.url
        return None
    
    def get_thumbnail_url(self, obj):
        """Retorna URL completa do thumbnail"""
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        return None


class PublicacaoPDFListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de publicações"""
    
    organizadores_display = serializers.CharField(source='get_organizadores_display', read_only=True)
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    arquivo_pdf_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PublicacaoPDF
        fields = [
            'id',
            'titulo',
            'subtitulo',
            'organizadores_display',
            'categoria',
            'categoria_display',
            'ano_publicacao',
            'thumbnail_url',
            'arquivo_pdf_url',
            'destaque',
            'downloads'
        ]
    
    def get_arquivo_pdf_url(self, obj):
        """Retorna URL completa do arquivo PDF"""
        if obj.arquivo_pdf:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.arquivo_pdf.url)
            return obj.arquivo_pdf.url
        return None
    
    def get_thumbnail_url(self, obj):
        """Retorna URL completa do thumbnail"""
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        return None


class ConfiguracaoPaginaPublicacoesSerializer(serializers.ModelSerializer):
    """Serializer para configurações da página de publicações"""
    
    imagem_hero_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ConfiguracaoPaginaPublicacoes
        fields = [
            'id',
            'titulo_pagina',
            'descricao_pagina',
            'imagem_hero_url',
            'publicacoes_por_pagina',
            'mostrar_estatisticas',
            'ativa'
        ]
        read_only_fields = ['id']
    
    def get_imagem_hero_url(self, obj):
        """Retorna URL completa da imagem hero"""
        if obj.imagem_hero:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagem_hero.url)
            return obj.imagem_hero.url
        return None


class EstatisticasSerializer(serializers.Serializer):
    """Serializer para estatísticas das publicações"""
    
    total_publicacoes = serializers.IntegerField()
    total_organizadores = serializers.IntegerField()
    anos_publicacao = serializers.IntegerField()
    downloads_total = serializers.IntegerField()
    categoria_mais_comum = serializers.DictField(required=False)
    
    def to_representation(self, instance):
        """Customiza a representação dos dados"""
        data = super().to_representation(instance)
        
        # Adiciona informações extras se disponíveis
        if hasattr(instance, 'publicacoes_por_categoria'):
            data['publicacoes_por_categoria'] = instance.publicacoes_por_categoria
        
        if hasattr(instance, 'publicacoes_por_ano'):
            data['publicacoes_por_ano'] = instance.publicacoes_por_ano
        
        return data


class PublicacaoPorAnoSerializer(serializers.Serializer):
    """Serializer para publicações agrupadas por ano"""
    
    ano = serializers.IntegerField()
    publicacoes = PublicacaoPDFListSerializer(many=True)
    total = serializers.SerializerMethodField()
    
    def get_total(self, obj):
        """Retorna o total de publicações do ano"""
        return len(obj.get('publicacoes', []))


class BuscaPublicacaoSerializer(serializers.Serializer):
    """Serializer para resultados de busca AJAX"""
    
    id = serializers.IntegerField()
    titulo = serializers.CharField()
    organizadores = serializers.CharField()
    ano = serializers.IntegerField()
    categoria = serializers.CharField()
    url = serializers.URLField(required=False, allow_null=True)
    thumbnail = serializers.URLField(required=False, allow_null=True)


class DownloadResponseSerializer(serializers.Serializer):
    """Serializer para resposta de incremento de download"""
    
    success = serializers.BooleanField()
    downloads = serializers.IntegerField(required=False)
    message = serializers.CharField(required=False)
    error = serializers.CharField(required=False)

