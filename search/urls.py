# urls.py para funcionalidade de busca - LANGUE UFRPE
from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_view, name='search_results'),
]