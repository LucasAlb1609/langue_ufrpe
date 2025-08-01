from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import LinhaPesquisa, Pesquisador, Estudante, ConfiguracaoPagina


class LinhasPesquisaListView(ListView):
    """View para listar todas as linhas de pesquisa ativas"""
    model = LinhaPesquisa
    template_name = 'linhas_pesquisa/linhas_pesquisa.html'
    context_object_name = 'linhas_pesquisa'
    paginate_by = 10
    
    def get_queryset(self):
        """Retorna apenas linhas de pesquisa ativas, ordenadas"""
        queryset = LinhaPesquisa.objects.filter(ativa=True).prefetch_related(
            'pesquisadores', 'estudantes'
        ).order_by('ordem', 'titulo')
        
        # Filtro de busca
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) |
                Q(objetivo__icontains=search_query) |
                Q(palavras_chave__icontains=search_query) |
                Q(setores_aplicacao__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Adiciona contexto extra para o template"""
        context = super().get_context_data(**kwargs)
        
        # Configuração da página
        try:
            context['configuracao'] = ConfiguracaoPagina.objects.first()
        except ConfiguracaoPagina.DoesNotExist:
            context['configuracao'] = None
        
        # Estatísticas
        context['total_linhas'] = LinhaPesquisa.objects.filter(ativa=True).count()
        context['total_pesquisadores'] = Pesquisador.objects.filter(ativo=True).count()
        context['total_estudantes'] = Estudante.objects.filter(ativo=True).count()
        
        # Query de busca para manter no formulário
        context['search_query'] = self.request.GET.get('search', '')
        
        return context


class LinhaPesquisaDetailView(DetailView):
    """View para exibir detalhes de uma linha de pesquisa específica"""
    model = LinhaPesquisa
    template_name = 'linhas_pesquisa/linha_pesquisa_detail.html'
    context_object_name = 'linha_pesquisa'
    
    def get_queryset(self):
        """Retorna apenas linhas de pesquisa ativas"""
        return LinhaPesquisa.objects.filter(ativa=True).prefetch_related(
            'pesquisadores', 'estudantes'
        )
    
    def get_context_data(self, **kwargs):
        """Adiciona contexto extra para o template"""
        context = super().get_context_data(**kwargs)
        
        # Configuração da página
        try:
            context['configuracao'] = ConfiguracaoPagina.objects.first()
        except ConfiguracaoPagina.DoesNotExist:
            context['configuracao'] = None
        
        # Linhas relacionadas (outras linhas)
        context['outras_linhas'] = LinhaPesquisa.objects.filter(
            ativa=True
        ).exclude(pk=self.object.pk).order_by('ordem', 'titulo')[:3]
        
        return context


@cache_page(60 * 15)  # Cache por 15 minutos
def linhas_pesquisa_view(request):
    """View baseada em função para linhas de pesquisa"""
    # Buscar configuração da página
    try:
        configuracao = ConfiguracaoPagina.objects.first()
    except ConfiguracaoPagina.DoesNotExist:
        configuracao = None
    
    # Buscar linhas de pesquisa ativas
    linhas_pesquisa = LinhaPesquisa.objects.filter(ativa=True).prefetch_related(
        'pesquisadores',
        'estudantes'
    ).order_by('ordem', 'titulo')
    
    # Filtro de busca
    search_query = request.GET.get('search')
    if search_query:
        linhas_pesquisa = linhas_pesquisa.filter(
            Q(titulo__icontains=search_query) |
            Q(objetivo__icontains=search_query) |
            Q(palavras_chave__icontains=search_query) |
            Q(setores_aplicacao__icontains=search_query)
        )
    
    # Paginação
    paginator = Paginator(linhas_pesquisa, 5)  # 5 linhas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    estatisticas = {
        'total_linhas': LinhaPesquisa.objects.filter(ativa=True).count(),
        'total_pesquisadores': Pesquisador.objects.filter(ativo=True).count(),
        'total_estudantes': Estudante.objects.filter(ativo=True).count(),
    }
    
    context = {
        'configuracao': configuracao,
        'linhas_pesquisa': page_obj,
        'page_obj': page_obj,
        'search_query': search_query or '',
        'estatisticas': estatisticas,
    }
    
    return render(request, 'linhas_pesquisa/linhas_pesquisa.html', context)


def linha_pesquisa_detail_view(request, pk):
    """View para detalhes de uma linha de pesquisa específica"""
    linha_pesquisa = get_object_or_404(
        LinhaPesquisa.objects.prefetch_related('pesquisadores', 'estudantes'),
        pk=pk,
        ativa=True
    )
    
    # Buscar configuração da página
    try:
        configuracao = ConfiguracaoPagina.objects.first()
    except ConfiguracaoPagina.DoesNotExist:
        configuracao = None
    
    # Outras linhas de pesquisa
    outras_linhas = LinhaPesquisa.objects.filter(
        ativa=True
    ).exclude(pk=pk).order_by('ordem', 'titulo')[:3]
    
    context = {
        'linha_pesquisa': linha_pesquisa,
        'configuracao': configuracao,
        'outras_linhas': outras_linhas,
    }
    
    return render(request, 'linhas_pesquisa/linha_pesquisa_detail.html', context)


def pesquisadores_ajax_view(request):
    """View AJAX para buscar pesquisadores"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        search_term = request.GET.get('search', '')
        
        pesquisadores = Pesquisador.objects.filter(
            ativo=True,
            nome__icontains=search_term
        ).order_by('nome')[:10]
        
        data = [{
            'id': p.id,
            'nome': p.nome,
            'universidade': p.universidade,
            'link_lattes': p.link_lattes or ''
        } for p in pesquisadores]
        
        return JsonResponse({'pesquisadores': data})
    
    return JsonResponse({'error': 'Requisição inválida'}, status=400)


def estudantes_ajax_view(request):
    """View AJAX para buscar estudantes"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        search_term = request.GET.get('search', '')
        nivel = request.GET.get('nivel', '')
        
        estudantes = Estudante.objects.filter(ativo=True)
        
        if search_term:
            estudantes = estudantes.filter(nome__icontains=search_term)
        
        if nivel:
            estudantes = estudantes.filter(nivel=nivel)
        
        estudantes = estudantes.order_by('nivel', 'nome')[:10]
        
        data = [{
            'id': e.id,
            'nome': e.nome,
            'nivel': e.get_nivel_display(),
            'universidade': e.universidade,
            'programa': e.programa or '',
            'link_lattes': e.link_lattes or ''
        } for e in estudantes]
        
        return JsonResponse({'estudantes': data})
    
    return JsonResponse({'error': 'Requisição inválida'}, status=400)


def estatisticas_ajax_view(request):
    """View AJAX para estatísticas da página"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        estatisticas = {
            'total_linhas': LinhaPesquisa.objects.filter(ativa=True).count(),
            'total_pesquisadores': Pesquisador.objects.filter(ativo=True).count(),
            'total_estudantes': Estudante.objects.filter(ativo=True).count(),
            'linhas_por_area': list(
                LinhaPesquisa.objects.filter(ativa=True)
                .values('titulo')
                .annotate(
                    total_pesquisadores=models.Count('pesquisadores', distinct=True),
                    total_estudantes=models.Count('estudantes', distinct=True)
                )
            )
        }
        
        return JsonResponse(estatisticas)
    
    return JsonResponse({'error': 'Requisição inválida'}, status=400)


# Views para API (se necessário)
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import LinhaPesquisaSerializer, PesquisadorSerializer, EstudanteSerializer


class LinhaPesquisaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para API REST das linhas de pesquisa"""
    queryset = LinhaPesquisa.objects.filter(ativa=True).order_by('ordem', 'titulo')
    serializer_class = LinhaPesquisaSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(titulo__icontains=search) |
                Q(objetivo__icontains=search) |
                Q(palavras_chave__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def pesquisadores(self, request, pk=None):
        """Endpoint para pesquisadores de uma linha específica"""
        linha = self.get_object()
        pesquisadores = linha.pesquisadores.filter(ativo=True)
        serializer = PesquisadorSerializer(pesquisadores, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def estudantes(self, request, pk=None):
        """Endpoint para estudantes de uma linha específica"""
        linha = self.get_object()
        estudantes = linha.estudantes.filter(ativo=True)
        serializer = EstudanteSerializer(estudantes, many=True)
        return Response(serializer.data)


class PesquisadorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para API REST dos pesquisadores"""
    queryset = Pesquisador.objects.filter(ativo=True).order_by('nome')
    serializer_class = PesquisadorSerializer
    permission_classes = [permissions.AllowAny]


class EstudanteViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para API REST dos estudantes"""
    queryset = Estudante.objects.filter(ativo=True).order_by('nivel', 'nome')
    serializer_class = EstudanteSerializer
    permission_classes = [permissions.AllowAny]

