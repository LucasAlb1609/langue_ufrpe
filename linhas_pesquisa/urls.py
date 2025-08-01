from django.urls import path, include
from django.views.generic import RedirectView
from . import views

# URLs do app de linhas de pesquisa
app_name = 'linhas_pesquisa'

urlpatterns = [
    # Página principal de linhas de pesquisa
    path('', views.linhas_pesquisa_view, name='linhas_pesquisa'),
    
    # Versão alternativa usando Class-Based View
    # path('', views.LinhasPesquisaListView.as_view(), name='linhas_pesquisa'),
    
    # Detalhes de uma linha de pesquisa específica
    path('<int:pk>/', views.linha_pesquisa_detail_view, name='linha_pesquisa_detail'),
    
    # Versão alternativa usando Class-Based View
    # path('<int:pk>/', views.LinhaPesquisaDetailView.as_view(), name='linha_pesquisa_detail'),
    
    # URLs AJAX para funcionalidades dinâmicas
    path('ajax/pesquisadores/', views.pesquisadores_ajax_view, name='pesquisadores_ajax'),
    path('ajax/estudantes/', views.estudantes_ajax_view, name='estudantes_ajax'),
    path('ajax/estatisticas/', views.estatisticas_ajax_view, name='estatisticas_ajax'),
    
    # Redirecionamentos para compatibilidade
    path('linhas/', RedirectView.as_view(pattern_name='linhas_pesquisa:linhas_pesquisa', permanent=True)),
    path('pesquisa/', RedirectView.as_view(pattern_name='linhas_pesquisa:linhas_pesquisa', permanent=True)),
]

# URLs para API REST (comentadas por enquanto)
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'api/linhas-pesquisa', views.LinhaPesquisaViewSet, basename='linhapesquisa')
# router.register(r'api/pesquisadores', views.PesquisadorViewSet, basename='pesquisador')
# router.register(r'api/estudantes', views.EstudanteViewSet, basename='estudante')
# urlpatterns += [path('', include(router.urls))]