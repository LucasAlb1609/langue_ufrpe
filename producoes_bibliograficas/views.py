from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib import messages
from collections import OrderedDict
from .models import ProducaoBibliografica, Autor, ConfiguracaoPaginaProducoes
from publicacoes.models import PublicacaoPDF

def producoes_e_publicacoes_view(request):
    # Lógica para Produções Bibliográficas
    producoes_por_ano = {}
    for producao in ProducaoBibliografica.objects.all().order_by('-ano_publicacao'):
        if producao.ano_publicacao not in producoes_por_ano:
            producoes_por_ano[producao.ano_publicacao] = []
        producoes_por_ano[producao.ano_publicacao].append(producao)

    # Lógica para Publicações PDF
    publicacoes_pdf = PublicacaoPDF.objects.all().order_by('-ano_publicacao')
    anos_disponiveis_pdf = sorted(list(set(publicacoes_pdf.values_list('ano_publicacao', flat=True))), reverse=True)

    context = {
        'producoes_por_ano': producoes_por_ano,
        'publicacoes_pdf': publicacoes_pdf,
        'anos_disponiveis_pdf': anos_disponiveis_pdf,
        'configuracao': None,  # Adicione sua lógica de configuração se houver
        'estatisticas_producoes': None, # Adicione sua lógica de estatísticas se houver
        'estatisticas_publicacoes_pdf': None, # Adicione sua lógica de estatísticas se houver
        'is_paginated_pdf': False # Adicione sua lógica de paginação se houver
    }
    return render(request, 'producoes_bibliograficas/producoes_bibliograficas.html', context)


class ProducoesBibliograficasListView(ListView):
    """View para listar todas as produções bibliográficas ativas"""
    model = ProducaoBibliografica
    template_name = 'producoes_bibliograficas/producoes_bibliograficas.html'
    context_object_name = 'producoes_bibliograficas'
    paginate_by = 50
    
    def get_queryset(self):
        """Retorna apenas produções ativas, ordenadas por ano decrescente"""
        queryset = ProducaoBibliografica.objects.filter(ativa=True).prefetch_related(
            'autores'
        ).order_by('-ano_publicacao', 'titulo')
        
        # Filtro de busca
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) |
                Q(autores__nome__icontains=search_query) |
                Q(local_publicacao__icontains=search_query) |
                Q(tipo__icontains=search_query)
            ).distinct()
        
        # Filtro por tipo
        tipo_filter = self.request.GET.get('tipo')
        if tipo_filter:
            queryset = queryset.filter(tipo=tipo_filter)
        
        # Filtro por ano
        ano_filter = self.request.GET.get('ano')
        if ano_filter:
            queryset = queryset.filter(ano_publicacao=ano_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Adiciona contexto extra para o template"""
        context = super().get_context_data(**kwargs)
        
        # Configuração da página
        try:
            context['configuracao'] = ConfiguracaoPaginaProducoes.objects.first()
        except ConfiguracaoPaginaProducoes.DoesNotExist:
            context['configuracao'] = None
        
        # Agrupar produções por ano
        producoes = self.get_queryset()
        producoes_por_ano = OrderedDict()
        
        for producao in producoes:
            ano = producao.ano_publicacao
            if ano not in producoes_por_ano:
                producoes_por_ano[ano] = []
            producoes_por_ano[ano].append(producao)
        
        context['producoes_por_ano'] = producoes_por_ano
        
        # Estatísticas
        context['estatisticas'] = self.get_estatisticas()
        
        # Filtros disponíveis
        context['anos_disponiveis'] = ProducaoBibliografica.objects.filter(
            ativa=True
        ).values_list('ano_publicacao', flat=True).distinct().order_by('-ano_publicacao')
        
        context['tipos_disponiveis'] = ProducaoBibliografica.TIPO_CHOICES
        
        # Query de busca para manter no formulário
        context['search_query'] = self.request.GET.get('search', '')
        context['tipo_filter'] = self.request.GET.get('tipo', '')
        context['ano_filter'] = self.request.GET.get('ano', '')
        
        return context
    
    def get_estatisticas(self):
        """Calcula estatísticas das produções"""
        producoes_ativas = ProducaoBibliografica.objects.filter(ativa=True)
        
        # Tipo mais comum
        tipo_mais_comum = producoes_ativas.values('tipo').annotate(
            count=Count('tipo')
        ).order_by('-count').first()
        
        return {
            'total_producoes': producoes_ativas.count(),
            'total_autores': Autor.objects.filter(producoes__ativa=True).distinct().count(),
            'anos_ativos': producoes_ativas.values('ano_publicacao').distinct().count(),
            'tipo_mais_comum': dict(ProducaoBibliografica.TIPO_CHOICES).get(
                tipo_mais_comum['tipo'] if tipo_mais_comum else 'ARTIGO'
            )
        }


class ProducaoBibliograficaDetailView(DetailView):
    """View para exibir detalhes de uma produção bibliográfica específica"""
    model = ProducaoBibliografica
    template_name = 'producoes_bibliograficas/producao_detail.html'
    context_object_name = 'producao'
    
    def get_queryset(self):
        """Retorna apenas produções ativas"""
        return ProducaoBibliografica.objects.filter(ativa=True).prefetch_related('autores')
    
    def get_context_data(self, **kwargs):
        """Adiciona contexto extra para o template"""
        context = super().get_context_data(**kwargs)
        
        # Configuração da página
        try:
            context['configuracao'] = ConfiguracaoPaginaProducoes.objects.first()
        except ConfiguracaoPaginaProducoes.DoesNotExist:
            context['configuracao'] = None
        
        # Produções relacionadas (mesmo ano ou mesmo tipo)
        context['producoes_relacionadas'] = ProducaoBibliografica.objects.filter(
            Q(ano_publicacao=self.object.ano_publicacao) | Q(tipo=self.object.tipo),
            ativa=True
        ).exclude(pk=self.object.pk).prefetch_related('autores')[:5]
        
        return context


@cache_page(60 * 15)  # Cache por 15 minutos
def producoes_bibliograficas_view(request):
    """View baseada em função para produções bibliográficas"""
    # Buscar configuração da página
    try:
        configuracao = ConfiguracaoPaginaProducoes.objects.first()
    except ConfiguracaoPaginaProducoes.DoesNotExist:
        configuracao = None
    
    # Buscar produções ativas
    producoes = ProducaoBibliografica.objects.filter(ativa=True).prefetch_related(
        'autores'
    ).order_by('-ano_publicacao', 'titulo')
    
    # Filtros
    search_query = request.GET.get('search')
    tipo_filter = request.GET.get('tipo')
    ano_filter = request.GET.get('ano')
    
    if search_query:
        producoes = producoes.filter(
            Q(titulo__icontains=search_query) |
            Q(autores__nome__icontains=search_query) |
            Q(local_publicacao__icontains=search_query) |
            Q(tipo__icontains=search_query)
        ).distinct()
    
    if tipo_filter:
        producoes = producoes.filter(tipo=tipo_filter)
    
    if ano_filter:
        producoes = producoes.filter(ano_publicacao=ano_filter)
    
    # Agrupar por ano
    producoes_por_ano = OrderedDict()
    for producao in producoes:
        ano = producao.ano_publicacao
        if ano not in producoes_por_ano:
            producoes_por_ano[ano] = []
        producoes_por_ano[ano].append(producao)
    
    # Estatísticas
    producoes_ativas = ProducaoBibliografica.objects.filter(ativa=True)
    tipo_mais_comum = producoes_ativas.values('tipo').annotate(
        count=Count('tipo')
    ).order_by('-count').first()
    
    estatisticas = {
        'total_producoes': producoes_ativas.count(),
        'total_autores': Autor.objects.filter(producoes__ativa=True).distinct().count(),
        'anos_ativos': producoes_ativas.values('ano_publicacao').distinct().count(),
        'tipo_mais_comum': dict(ProducaoBibliografica.TIPO_CHOICES).get(
            tipo_mais_comum['tipo'] if tipo_mais_comum else 'ARTIGO'
        )
    }
    
    # Filtros disponíveis
    anos_disponiveis = ProducaoBibliografica.objects.filter(
        ativa=True
    ).values_list('ano_publicacao', flat=True).distinct().order_by('-ano_publicacao')
    
    context = {
        'configuracao': configuracao,
        'producoes_por_ano': producoes_por_ano,
        'estatisticas': estatisticas,
        'anos_disponiveis': anos_disponiveis,
        'tipos_disponiveis': ProducaoBibliografica.TIPO_CHOICES,
        'search_query': search_query or '',
        'tipo_filter': tipo_filter or '',
        'ano_filter': ano_filter or '',
    }
    
    return render(request, 'producoes_bibliograficas/producoes_bibliograficas.html', context)


def producao_detail_view(request, pk):
    """View para detalhes de uma produção específica"""
    producao = get_object_or_404(
        ProducaoBibliografica.objects.prefetch_related('autores'),
        pk=pk,
        ativa=True
    )
    
    # Buscar configuração da página
    try:
        configuracao = ConfiguracaoPaginaProducoes.objects.first()
    except ConfiguracaoPaginaProducoes.DoesNotExist:
        configuracao = None
    
    # Produções relacionadas
    producoes_relacionadas = ProducaoBibliografica.objects.filter(
        Q(ano_publicacao=producao.ano_publicacao) | Q(tipo=producao.tipo),
        ativa=True
    ).exclude(pk=pk).prefetch_related('autores')[:5]
    
    context = {
        'producao': producao,
        'configuracao': configuracao,
        'producoes_relacionadas': producoes_relacionadas,
    }
    
    return render(request, 'producoes_bibliograficas/producao_detail.html', context)


def autores_ajax_view(request):
    """View AJAX para buscar autores"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        search_term = request.GET.get('search', '')
        
        autores = Autor.objects.filter(
            nome__icontains=search_term
        ).order_by('nome')[:10]
        
        data = [{
            'id': a.id,
            'nome': a.nome,
            'lattes_link': a.lattes_link or '',
            'total_producoes': a.producoes.filter(ativa=True).count()
        } for a in autores]
        
        return JsonResponse({'autores': data})
    
    return JsonResponse({'error': 'Requisição inválida'}, status=400)


def producoes_por_ano_ajax_view(request):
    """View AJAX para obter produções de um ano específico"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        ano = request.GET.get('ano')
        
        if not ano:
            return JsonResponse({'error': 'Ano não especificado'}, status=400)
        
        try:
            ano = int(ano)
        except ValueError:
            return JsonResponse({'error': 'Ano inválido'}, status=400)
        
        producoes = ProducaoBibliografica.objects.filter(
            ano_publicacao=ano,
            ativa=True
        ).prefetch_related('autores').order_by('titulo')
        
        data = [{
            'id': p.id,
            'titulo': p.titulo,
            'autores': [a.nome for a in p.autores.all()],
            'tipo': p.get_tipo_display(),
            'local_publicacao': p.local_publicacao or '',
            'link_producao': p.link_producao or ''
        } for p in producoes]
        
        return JsonResponse({'producoes': data, 'ano': ano})
    
    return JsonResponse({'error': 'Requisição inválida'}, status=400)


def estatisticas_ajax_view(request):
    """View AJAX para estatísticas das produções"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        producoes_ativas = ProducaoBibliografica.objects.filter(ativa=True)
        
        # Distribuição por tipo
        distribuicao_tipos = list(
            producoes_ativas.values('tipo').annotate(
                count=Count('tipo')
            ).order_by('-count')
        )
        
        # Distribuição por ano
        distribuicao_anos = list(
            producoes_ativas.values('ano_publicacao').annotate(
                count=Count('ano_publicacao')
            ).order_by('-ano_publicacao')
        )
        
        # Autores mais produtivos
        autores_produtivos = list(
            Autor.objects.filter(producoes__ativa=True).annotate(
                total_producoes=Count('producoes')
            ).order_by('-total_producoes')[:5].values('nome', 'total_producoes')
        )
        
        estatisticas = {
            'total_producoes': producoes_ativas.count(),
            'total_autores': Autor.objects.filter(producoes__ativa=True).distinct().count(),
            'distribuicao_tipos': distribuicao_tipos,
            'distribuicao_anos': distribuicao_anos,
            'autores_mais_produtivos': autores_produtivos,
        }
        
        return JsonResponse(estatisticas)
    
    return JsonResponse({'error': 'Requisição inválida'}, status=400)

def producao_detail(request, producao_id):
    producao = get_object_or_404(ProducaoBibliografica, pk=producao_id)
    return render(request, (
        'producoes_bibliograficas/producao_detail.html'
    ), {'producao': producao})

# Views para API (se necessário)
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProducaoBibliograficaSerializer, AutorSerializer


class ProducaoBibliograficaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para API REST das produções bibliográficas"""
    queryset = ProducaoBibliografica.objects.filter(ativa=True).order_by('-ano_publicacao', 'titulo')
    serializer_class = ProducaoBibliograficaSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(titulo__icontains=search) |
                Q(autores__nome__icontains=search) |
                Q(local_publicacao__icontains=search)
            ).distinct()
        
        tipo = self.request.query_params.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        ano = self.request.query_params.get('ano')
        if ano:
            queryset = queryset.filter(ano_publicacao=ano)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def por_ano(self, request):
        """Endpoint para produções agrupadas por ano"""
        producoes = self.get_queryset()
        producoes_por_ano = {}
        
        for producao in producoes:
            ano = str(producao.ano_publicacao)
            if ano not in producoes_por_ano:
                producoes_por_ano[ano] = []
            producoes_por_ano[ano].append(
                ProducaoBibliograficaSerializer(producao, context={'request': request}).data
            )
        
        return Response(producoes_por_ano)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Endpoint para estatísticas"""
        producoes_ativas = ProducaoBibliografica.objects.filter(ativa=True)
        
        estatisticas = {
            'total_producoes': producoes_ativas.count(),
            'total_autores': Autor.objects.filter(producoes__ativa=True).distinct().count(),
            'distribuicao_tipos': list(
                producoes_ativas.values('tipo').annotate(count=Count('tipo'))
            ),
            'distribuicao_anos': list(
                producoes_ativas.values('ano_publicacao').annotate(count=Count('ano_publicacao'))
            )
        }
        
        return Response(estatisticas)


class AutorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para API REST dos autores"""
    queryset = Autor.objects.all().order_by('nome')
    serializer_class = AutorSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=True, methods=['get'])
    def producoes(self, request, pk=None):
        """Endpoint para produções de um autor específico"""
        autor = self.get_object()
        producoes = autor.producoes.filter(ativa=True).order_by('-ano_publicacao')
        serializer = ProducaoBibliograficaSerializer(producoes, many=True, context={'request': request})
        return Response(serializer.data)

