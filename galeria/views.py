from django.shortcuts import render, get_object_or_404
from .models import Album

def album_list_view(request):
    """
    Exibe a lista de todos os álbuns de fotos.
    """
    albums = Album.objects.all()
    context = {
        'albums': albums
    }
    return render(request, 'galeria/album_list.html', context)

def album_detail_view(request, pk):
    """
    Exibe todas as fotos de um álbum específico.
    """
    album = get_object_or_404(Album, pk=pk)
    photos = album.photos.all()
    context = {
        'album': album,
        'photos': photos
    }
    return render(request, 'galeria/album_detail.html', context)

def detalhe_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, (
        'galeria/detalhe_album.html'
    ), {'album': album})