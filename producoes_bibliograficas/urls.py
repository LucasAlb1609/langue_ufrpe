from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import producoes_e_publicacoes_view

# Configuração do router para API REST
router = DefaultRouter()
router.register(r'producoes', views.ProducaoBibliograficaViewSet)
router.register(r'autores', views.AutorViewSet)

app_name = 'producoes_bibliograficas'

urlpatterns = [
    # URLs principais da aplicação
    path('', producoes_e_publicacoes_view, name='producoes_e_publicacoes'),
    path('lista/', views.ProducoesBibliograficasListView.as_view(), name='lista'),
    path('producao/<int:id>/', views.producao_detail_view, name='producao_detail'),
    
    # URLs AJAX
    path('ajax/autores/', views.autores_ajax_view, name='autores_ajax'),
    path('ajax/producoes-por-ano/', views.producoes_por_ano_ajax_view, name='producoes_por_ano_ajax'),
    path('ajax/estatisticas/', views.estatisticas_ajax_view, name='estatisticas_ajax'),
    
    # API REST (opcional)
    path('api/', include(router.urls)),
]

