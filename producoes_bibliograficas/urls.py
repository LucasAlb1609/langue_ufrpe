from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuração do router para API REST
router = DefaultRouter()
router.register(r'producoes', views.ProducaoBibliograficaViewSet)
router.register(r'autores', views.AutorViewSet)

app_name = 'producoes_bibliograficas'

urlpatterns = [
    # URLs principais da aplicação
    path('', views.producoes_bibliograficas_view, name='producoes_bibliograficas'),
    path('lista/', views.ProducoesBibliograficasListView.as_view(), name='lista'),
    path('producao/<int:pk>/', views.producao_detail_view, name='producao_detail'),
    
    # URLs AJAX
    path('ajax/autores/', views.autores_ajax_view, name='autores_ajax'),
    path('ajax/producoes-por-ano/', views.producoes_por_ano_ajax_view, name='producoes_por_ano_ajax'),
    path('ajax/estatisticas/', views.estatisticas_ajax_view, name='estatisticas_ajax'),
    
    # API REST (opcional)
    path('api/', include(router.urls)),
]

