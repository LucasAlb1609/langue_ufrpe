from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from producoes_bibliograficas.models import ProducaoBibliografica
from publicacoes.models import PublicacaoPDF
from galeria.models import Album

# Create your views here.

def home(request):
    latest_producao = ProducaoBibliografica.objects.order_by('-ano_publicacao', '-id').first()
    latest_publicacao = PublicacaoPDF.objects.order_by('-ano_publicacao', '-id').first()
    latest_galeria = Album.objects.order_by('-created_at', '-id').first()
    context = {
        'latest_producao': latest_producao,
        'latest_publicacao': latest_publicacao,
        'latest_galeria': latest_galeria,
    }
    return render(request, 'home/index.html', context)


