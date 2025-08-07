from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PublicacaoPDF, Organizador, ConfiguracaoPaginaPublicacoes
from .serializers import PublicacaoPDFSerializer, OrganizadorSerializer
import json


class PublicacoesListView(ListView):
    """View baseada em classe para listar publicações com filtros e paginação"""
    model = PublicacaoPDF
    template_name = 'publicacoes/publicacoes.html'
    context_object_name = 'publicacoes'
    paginate_by = 12

    def get_queryset(self):
        """Retorna queryset filtrado e ordenado"""
        queryset = PublicacaoPDF.objects.filter(ativa=True).select_related().prefetch_related('organizadores')
        
        # Filtros da URL
        categoria = self.request.GET.get('categoria')
        ano = self.request.GET.get('ano')
        busca = self.request.GET.get('busca')
        ordenacao = self.request.GET.get('ordenacao', '-ano_publicacao')
        
        # Aplicar filtros
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        if ano:
            try:
                ano_int = int(ano)
                queryset = queryset.filter(ano_publicacao=ano_int)
            except ValueError:
                pass
        
        if busca:
            queryset = queryset.filter(
                Q(titulo__icontains=busca) |
                Q(subtitulo__icontains=busca) |
                Q(descricao__icontains=busca) |
                Q(organizadores__nome__icontains=busca) |
                Q(editora__icontains=busca)
            ).distinct()
        
        # Aplicar ordenação
        campos_ordenacao_validos = [
            'ano_publicacao', '-ano_publicacao',
            'titulo', '-titulo',
            'downloads', '-downloads',
            'criado_em', '-criado_em'
        ]
        
        if ordenacao in campos_ordenacao_validos:
            queryset = queryset.order_by(ordenacao)
        else:
            queryset = queryset.order_by('-ano_publicacao', '-criado_em')
        
        return queryset

    def get_context_data(self, **kwargs):
        """Adiciona dados extras ao contexto"""
        context = super().get_context_data(**kwargs)
        
        # Configuração da página
        try:
            configuracao = ConfiguracaoPaginaPublicacoes.objects.get(ativa=True)
        except ConfiguracaoPaginaPublicacoes.DoesNotExist:
            configuracao = ConfiguracaoPaginaPublicacoes(
                titulo_pagina="Publicações",
                descricao_pagina="Explore nossa coleção de publicações acadêmicas em PDF."
            )
        
        context['configuracao'] = configuracao
        
        # Anos disponíveis para filtro (convertido para lista para segurança)
        anos_disponiveis = list(
            PublicacaoPDF.objects.filter(ativa=True)
            .values_list('ano_publicacao', flat=True)
            .distinct()
            .order_by('-ano_publicacao')
        )

        context['anos_disponiveis'] = anos_disponiveis
        
        # Estatísticas
        if configuracao.mostrar_estatisticas:
            context.update(self.get_estatisticas())
        
        # Filtros ativos (para manter estado no template)
        context['filtros_ativos'] = {
            'categoria': self.request.GET.get('categoria', ''),
            'ano': self.request.GET.get('ano', ''),
            'busca': self.request.GET.get('busca', ''),
            'ordenacao': self.request.GET.get('ordenacao', '-ano_publicacao'),
        }
        
        return context

    def get_estatisticas(self):
        """Calcula estatísticas das publicações de forma segura."""
        publicacoes_ativas = PublicacaoPDF.objects.filter(ativa=True)
        
        # Total de publicações
        total_publicacoes = publicacoes_ativas.count()
        
        # Total de organizadores únicos
        total_organizadores = Organizador.objects.filter(
            publicacoes__ativa=True,
            ativo=True
        ).distinct().count()
        
        # Contagem de anos distintos com publicações
        anos_publicacao_count = publicacoes_ativas.values_list(
            'ano_publicacao', flat=True
        ).distinct().count()
        
        # Categoria mais comum (lógica corrigida e segura)
        categoria_info = {'nome': 'N/A'} # Valor padrão
        if publicacoes_ativas.exists():
            # .first() é usado para pegar o primeiro item ou None, evitando erros.
            categoria_query = publicacoes_ativas.values('categoria').annotate(
                count=Count('categoria')
            ).order_by('-count').first()
            
            if categoria_query:
                nome_categoria = dict(PublicacaoPDF.CATEGORIA_CHOICES).get(
                    categoria_query['categoria'], 'N/A'
                )
                categoria_info = {'nome': nome_categoria}
        
        return {
            'total_publicacoes': total_publicacoes,
            'total_organizadores': total_organizadores,
            'anos_publicacao': anos_publicacao_count, # Nome da variável claro
            'categoria_mais_comum': categoria_info,
        }


def publicacoes_view(request):
    """View baseada em função (alternativa à ListView)"""
    # Obter configuração
    try:
        configuracao = ConfiguracaoPaginaPublicacoes.objects.get(ativa=True)
        paginate_by = configuracao.publicacoes_por_pagina
    except ConfiguracaoPaginaPublicacoes.DoesNotExist:
        configuracao = None
        paginate_by = 12
    
    # Obter publicações
    publicacoes = PublicacaoPDF.objects.filter(ativa=True).select_related().prefetch_related('organizadores')
    
    # Filtros
    categoria = request.GET.get('categoria')
    ano = request.GET.get('ano')
    busca = request.GET.get('busca')
    ordenacao = request.GET.get('ordenacao', '-ano_publicacao')
    
    if categoria:
        publicacoes = publicacoes.filter(categoria=categoria)
    
    if ano:
        try:
            ano_int = int(ano)
            publicacoes = publicacoes.filter(ano_publicacao=ano_int)
        except ValueError:
            pass
    
    if busca:
        publicacoes = publicacoes.filter(
            Q(titulo__icontains=busca) |
            Q(subtitulo__icontains=busca) |
            Q(descricao__icontains=busca) |
            Q(organizadores__nome__icontains=busca) |
            Q(editora__icontains=busca)
        ).distinct()
    
    # Ordenação
    campos_validos = ['ano_publicacao', '-ano_publicacao', 'titulo', '-titulo', 'downloads', '-downloads']
    if ordenacao in campos_validos:
        publicacoes = publicacoes.order_by(ordenacao)
    else:
        publicacoes = publicacoes.order_by('-ano_publicacao', '-criado_em')
    
    # Paginação
    paginator = Paginator(publicacoes, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Anos disponíveis
    anos_disponiveis = PublicacaoPDF.objects.filter(ativa=True).values_list(
        'ano_publicacao', flat=True
    ).distinct().order_by('-ano_publicacao')
    
    # Estatísticas
    estatisticas = {}
    if configuracao and configuracao.mostrar_estatisticas:
        publicacoes_ativas = PublicacaoPDF.objects.filter(ativa=True)
        estatisticas['total_publicacoes'] = publicacoes_ativas.count()
        estatisticas['total_organizadores'] = Organizador.objects.filter(
            publicacoes__ativa=True, ativo=True
        ).distinct().count()
        estatisticas['anos_publicacao'] = publicacoes_ativas.values_list(
            'ano_publicacao', flat=True
        ).distinct().count()
        
        # Categoria mais comum
        categoria_info = {'nome': 'N/A'}
        if publicacoes_ativas.exists():
            categoria_mais_comum = publicacoes_ativas.values('categoria').annotate(
                count=Count('categoria')
            ).order_by('-count').first()
            if categoria_mais_comum:
                categoria_nome = dict(PublicacaoPDF.CATEGORIA_CHOICES).get(
                    categoria_mais_comum['categoria'], 'N/A'
                )
                categoria_info = {'nome': categoria_nome}
        estatisticas['categoria_mais_comum'] = categoria_info
    
    context = {
        'publicacoes': page_obj,
        'configuracao': configuracao,
        'anos_disponiveis': anos_disponiveis,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'filtros_ativos': {
            'categoria': categoria or '',
            'ano': ano or '',
            'busca': busca or '',
            'ordenacao': ordenacao,
        },
        **estatisticas
    }
    
    return render(request, 'publicacoes/publicacoes.html', context)


@require_POST
def incrementar_download(request, publicacao_id):
    """Incrementa o contador de downloads de uma publicação"""
    try:
        publicacao = get_object_or_404(PublicacaoPDF, id=publicacao_id, ativa=True)
        publicacao.incrementar_download()
        
        return JsonResponse({
            'success': True,
            'downloads': publicacao.downloads,
            'message': 'Download incrementado com sucesso'
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def publicacao_detalhes(request, publicacao_id):
    """View para exibir detalhes de uma publicação específica"""
    publicacao = get_object_or_404(PublicacaoPDF, id=publicacao_id, ativa=True)
    
    # Publicações relacionadas (mesma categoria ou organizadores)
    publicacoes_relacionadas = PublicacaoPDF.objects.filter(
        Q(categoria=publicacao.categoria) | 
        Q(organizadores__in=publicacao.organizadores.all()),
        ativa=True
    ).exclude(id=publicacao.id).distinct()[:4]
    
    context = {
        'publicacao': publicacao,
        'publicacoes_relacionadas': publicacoes_relacionadas,
    }
    
    return render(request, 'publicacoes/publicacao_detalhes.html', context)


def buscar_publicacoes_ajax(request):
    """Busca AJAX para publicações (para autocomplete ou busca dinâmica)"""
    termo = request.GET.get('q', '').strip()
    
    if len(termo) < 2:
        return JsonResponse({'results': []})
    
    publicacoes = PublicacaoPDF.objects.filter(
        Q(titulo__icontains=termo) |
        Q(organizadores__nome__icontains=termo),
        ativa=True
    ).distinct()[:10]
    
    results = []
    for pub in publicacoes:
        results.append({
            'id': pub.id,
            'titulo': pub.titulo,
            'organizadores': pub.get_organizadores_display(),
            'ano': pub.ano_publicacao,
            'categoria': pub.get_categoria_display(),
            'url': pub.arquivo_pdf.url if pub.arquivo_pdf else None,
            'thumbnail': pub.thumbnail.url if pub.thumbnail else None,
        })
    
    return JsonResponse({'results': results})


# === API REST (usando Django REST Framework) ===

class PublicacaoPDFViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para API REST das publicações"""
    queryset = PublicacaoPDF.objects.filter(ativa=True)
    serializer_class = PublicacaoPDFSerializer
    filterset_fields = ['categoria', 'ano_publicacao', 'destaque']
    search_fields = ['titulo', 'subtitulo', 'descricao', 'organizadores__nome']
    ordering_fields = ['ano_publicacao', 'titulo', 'downloads', 'criado_em']
    ordering = ['-ano_publicacao', '-criado_em']

    @action(detail=True, methods=['post'])
    def incrementar_download(self, request, pk=None):
        """Endpoint para incrementar downloads via API"""
        publicacao = self.get_object()
        publicacao.incrementar_download()
        
        return Response({
            'downloads': publicacao.downloads,
            'message': 'Download incrementado com sucesso'
        })

    @action(detail=False)
    def estatisticas(self, request):
        """Endpoint para obter estatísticas das publicações"""
        publicacoes_ativas = self.get_queryset()
        
        stats = {
            'total_publicacoes': publicacoes_ativas.count(),
            'total_organizadores': Organizador.objects.filter(
                publicacoes__ativa=True, ativo=True
            ).distinct().count(),
            'anos_publicacao': publicacoes_ativas.values_list(
                'ano_publicacao', flat=True
            ).distinct().count(),
            'downloads_total': sum(pub.downloads for pub in publicacoes_ativas),
        }
        
        # Categoria mais comum
        # Verifica se há publicações ativas antes de tentar acessar o primeiro elemento
        categoria_mais_comum_query = publicacoes_ativas.values('categoria').annotate(
            count=Count('categoria')
        ).order_by('-count')
        
        if categoria_mais_comum_query.exists():
            categoria_mais_comum = categoria_mais_comum_query.first()
            stats['categoria_mais_comum'] = {
                'categoria': categoria_mais_comum['categoria'],
                'nome': dict(PublicacaoPDF.CATEGORIA_CHOICES).get(
                    categoria_mais_comum['categoria']
                ),
                'count': categoria_mais_comum['count']
            }
        else:
            stats['categoria_mais_comum'] = {'nome': 'N/A'}
        
        return Response(stats)

    @action(detail=False)
    def por_ano(self, request):
        """Endpoint para obter publicações agrupadas por ano"""
        publicacoes_por_ano = {}
        
        for publicacao in self.get_queryset():
            ano = publicacao.ano_publicacao
            if ano not in publicacoes_por_ano:
                publicacoes_por_ano[ano] = []
            
            publicacoes_por_ano[ano].append(
                self.get_serializer(publicacao).data
            )
        
        # Ordenar por ano (mais recente primeiro)
        resultado = [
            {'ano': ano, 'publicacoes': publicacoes}
            for ano, publicacoes in sorted(
                publicacoes_por_ano.items(), 
                key=lambda x: x[0], 
                reverse=True
            )
        ]
        
        return Response(resultado)


class OrganizadorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para API REST dos organizadores"""
    queryset = Organizador.objects.filter(ativo=True)
    serializer_class = OrganizadorSerializer
    search_fields = ['nome', 'biografia']
    ordering = ['nome']

    @action(detail=True)
    def publicacoes(self, request, pk=None):
        """Endpoint para obter publicações de um organizador"""
        organizador = self.get_object()
        publicacoes = organizador.publicacoes.filter(ativa=True)
        
        serializer = PublicacaoPDFSerializer(publicacoes, many=True)
        return Response(serializer.data)