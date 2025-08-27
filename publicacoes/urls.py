from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuração do router para API REST
router = DefaultRouter()
router.register(r'publicacoes', views.PublicacaoPDFViewSet)
router.register(r'organizadores', views.OrganizadorViewSet)

app_name = 'publicacoes'

urlpatterns = [
    # URLs principais da aplicação
    path('', views.PublicacoesListView.as_view(), name='lista'),
    
    # URLs alternativas (usando views baseadas em função)
    # path('', views.publicacoes_view, name='lista'),
    
    # Detalhes de uma publicação específica
    path('<int:publicacao_id>/', views.publicacao_detalhes, name='detalhes'),
    
    # AJAX endpoints
    path('incrementar-download/<int:publicacao_id>/', views.incrementar_download, name='incrementar_download'),
    path('buscar/', views.buscar_publicacoes_ajax, name='buscar_ajax'),
    
    # API REST endpoints
    path('api/', include(router.urls)),
]