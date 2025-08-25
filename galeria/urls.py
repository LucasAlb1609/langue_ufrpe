from django.urls import path
from .views import album_list_view, album_detail_view

app_name = 'galeria'

urlpatterns = [
    # URL para a lista de álbuns (página principal da galeria)
    # Ex: /galeria/
    path('', album_list_view, name='album_list'),
    
    # URL para ver as fotos de um álbum específico
    # Ex: /galeria/1/
    path('<int:pk>/', album_detail_view, name='album_detail'),
]
