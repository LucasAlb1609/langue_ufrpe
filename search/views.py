# views.py para funcionalidade de busca - LANGUE UFRPE
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from linhas_pesquisa.models import LinhaPesquisa
from producoes_bibliograficas.models import ProducaoBibliografica
from publicacoes.models import PublicacaoPDF

def search_view(request):
    """
    View para busca unificada em todo o site
    """
    query = request.GET.get('q', '').strip()
    results = {
        'linhas_pesquisa': [],
        'producoes_bibliograficas': [],
        'publicacoes_pdf': [],
        'total_results': 0
    }
    
    if query:
        # Busca em Linhas de Pesquisa
        linhas_pesquisa = LinhaPesquisa.objects.filter(
            Q(titulo__icontains=query) |
            Q(objetivo__icontains=query) |
            Q(palavras_chave__icontains=query) |
            Q(setores_aplicacao__icontains=query)
        ).distinct()
        
        # Busca em Produções Bibliográficas
        producoes = ProducaoBibliografica.objects.filter(
            Q(titulo__icontains=query) |
            Q(local_publicacao__icontains=query) |
            Q(autores__nome__icontains=query)
        ).distinct()
        
        # Busca em Publicações PDF
        publicacoes = PublicacaoPDF.objects.filter(
            Q(titulo__icontains=query) |
            Q(organizadores__nome__icontains=query) |
            Q(categoria__icontains=query)
        ).distinct()
        
        results['linhas_pesquisa'] = linhas_pesquisa
        results['producoes_bibliograficas'] = producoes
        results['publicacoes_pdf'] = publicacoes
        results['total_results'] = (
            linhas_pesquisa.count() + 
            producoes.count() + 
            publicacoes.count()
        )
    
    context = {
        'query': query,
        'results': results,
        'has_results': results['total_results'] > 0
    }
    
    return render(request, 'search/search_results.html', context)

