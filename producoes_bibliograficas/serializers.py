from rest_framework import serializers
from .models import ProducaoBibliografica, Autor, ConfiguracaoPaginaProducoes


class AutorSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Autor"""
    total_producoes = serializers.SerializerMethodField()
    
    class Meta:
        model = Autor
        fields = ['id', 'nome', 'lattes_link', 'total_producoes']
    
    def get_total_producoes(self, obj):
        """Retorna o total de produções ativas do autor"""
        return obj.producoes.filter(ativa=True).count()


class ProducaoBibliograficaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo ProducaoBibliografica"""
    autores = AutorSerializer(many=True, read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    autores_display = serializers.CharField(source='get_autores_display', read_only=True)
    
    class Meta:
        model = ProducaoBibliografica
        fields = [
            'id', 'titulo', 'link_producao', 'tipo', 'tipo_display',
            'local_publicacao', 'volume', 'numero', 'paginas',
            'ano_publicacao', 'autores', 'autores_display',
            'data_criacao', 'data_atualizacao'
        ]


class ProducaoBibliograficaDetailSerializer(ProducaoBibliograficaSerializer):
    """Serializer detalhado para o modelo ProducaoBibliografica"""
    producoes_relacionadas = serializers.SerializerMethodField()
    
    class Meta(ProducaoBibliograficaSerializer.Meta):
        fields = ProducaoBibliograficaSerializer.Meta.fields + ['producoes_relacionadas']
    
    def get_producoes_relacionadas(self, obj):
        """Retorna produções relacionadas (mesmo ano ou tipo)"""
        from django.db.models import Q
        
        relacionadas = ProducaoBibliografica.objects.filter(
            Q(ano_publicacao=obj.ano_publicacao) | Q(tipo=obj.tipo),
            ativa=True
        ).exclude(pk=obj.pk).prefetch_related('autores')[:5]
        
        return ProducaoBibliograficaSerializer(relacionadas, many=True, context=self.context).data


class ConfiguracaoPaginaProducoesSerializer(serializers.ModelSerializer):
    """Serializer para o modelo ConfiguracaoPaginaProducoes"""
    
    class Meta:
        model = ConfiguracaoPaginaProducoes
        fields = ['id', 'titulo_pagina', 'descricao_pagina', 'imagem_hero']


class EstatisticasSerializer(serializers.Serializer):
    """Serializer para estatísticas das produções bibliográficas"""
    total_producoes = serializers.IntegerField()
    total_autores = serializers.IntegerField()
    anos_ativos = serializers.IntegerField()
    tipo_mais_comum = serializers.CharField()
    distribuicao_tipos = serializers.ListField(child=serializers.DictField())
    distribuicao_anos = serializers.ListField(child=serializers.DictField())
    autores_mais_produtivos = serializers.ListField(child=serializers.DictField())


class ProducoesPorAnoSerializer(serializers.Serializer):
    """Serializer para produções agrupadas por ano"""
    ano = serializers.IntegerField()
    producoes = ProducaoBibliograficaSerializer(many=True)
    total = serializers.IntegerField()


class BuscaSerializer(serializers.Serializer):
    """Serializer para parâmetros de busca"""
    search = serializers.CharField(required=False, allow_blank=True)
    tipo = serializers.ChoiceField(choices=ProducaoBibliografica.TIPO_CHOICES, required=False)
    ano = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False, min_value=1)
    page_size = serializers.IntegerField(required=False, min_value=1, max_value=100)

