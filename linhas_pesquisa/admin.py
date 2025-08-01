from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import LinhaPesquisa, Pesquisador, Estudante, ConfiguracaoPagina


@admin.register(Pesquisador)
class PesquisadorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'universidade', 'link_lattes_display', 'ativo']
    list_filter = ['universidade', 'ativo']
    search_fields = ['nome', 'universidade']
    list_editable = ['ativo']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'universidade')
        }),
        ('Links e Configurações', {
            'fields': ('link_lattes', 'ativo')
        }),
    )
    
    def link_lattes_display(self, obj):
        if obj.link_lattes:
            return format_html(
                '<a href="{}" target="_blank">Ver Lattes</a>',
                obj.link_lattes
            )
        return "Não informado"
    link_lattes_display.short_description = "Currículo Lattes"


@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nivel', 'universidade', 'programa', 'link_lattes_display', 'ativo']
    list_filter = ['nivel', 'universidade', 'ativo']
    search_fields = ['nome', 'universidade', 'programa']
    list_editable = ['ativo']
    ordering = ['nivel', 'nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'nivel')
        }),
        ('Instituição', {
            'fields': ('universidade', 'programa')
        }),
        ('Links e Configurações', {
            'fields': ('link_lattes', 'ativo')
        }),
    )
    
    def link_lattes_display(self, obj):
        if obj.link_lattes:
            return format_html(
                '<a href="{}" target="_blank">Ver Lattes</a>',
                obj.link_lattes
            )
        return "Não informado"
    link_lattes_display.short_description = "Currículo Lattes"


class PesquisadorInline(admin.TabularInline):
    model = LinhaPesquisa.pesquisadores.through
    extra = 1
    verbose_name = "Pesquisador"
    verbose_name_plural = "Pesquisadores"


class EstudanteInline(admin.TabularInline):
    model = LinhaPesquisa.estudantes.through
    extra = 1
    verbose_name = "Estudante"
    verbose_name_plural = "Estudantes"


@admin.register(LinhaPesquisa)
class LinhaPesquisaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ativa', 'ordem', 'total_pesquisadores', 'total_estudantes', 'data_atualizacao']
    list_filter = ['ativa', 'data_criacao']
    search_fields = ['titulo', 'objetivo', 'palavras_chave']
    list_editable = ['ativa', 'ordem']
    ordering = ['ordem', 'titulo']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'objetivo')
        }),
        ('Detalhes da Pesquisa', {
            'fields': ('palavras_chave', 'setores_aplicacao')
        }),
        ('Mídia', {
            'fields': ('imagem',)
        }),
        ('Relacionamentos', {
            'fields': ('pesquisadores', 'estudantes')
        }),
        ('Configurações', {
            'fields': ('ativa', 'ordem'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['pesquisadores', 'estudantes']
    
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    def total_pesquisadores(self, obj):
        return obj.pesquisadores.filter(ativo=True).count()
    total_pesquisadores.short_description = "Pesquisadores"
    
    def total_estudantes(self, obj):
        return obj.estudantes.filter(ativo=True).count()
    total_estudantes.short_description = "Estudantes"
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Customizar help_text para palavras-chave
        if 'palavras_chave' in form.base_fields:
            form.base_fields['palavras_chave'].help_text = (
                "Digite as palavras-chave separadas por ponto e vírgula (;). "
                "Exemplo: História da literatura; Crítica social; Literatura brasileira"
            )
        
        return form
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Log da ação
        if change:
            self.message_user(request, f'Linha de pesquisa "{obj.titulo}" atualizada com sucesso.')
        else:
            self.message_user(request, f'Linha de pesquisa "{obj.titulo}" criada com sucesso.')


@admin.register(ConfiguracaoPagina)
class ConfiguracaoPaginaAdmin(admin.ModelAdmin):
    list_display = ['titulo_pagina']
    
    fieldsets = (
        ('Configurações da Página', {
            'fields': ('titulo_pagina', 'descricao_pagina')
        }),
        ('Mídia', {
            'fields': ('imagem_hero',)
        }),
    )
    
    def has_add_permission(self, request):
        # Permitir adicionar apenas se não existir nenhuma configuração
        return not ConfiguracaoPagina.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Não permitir deletar a configuração
        return False


# Customização do admin site
admin.site.site_header = "LANGUE UFRPE - Administração"
admin.site.site_title = "LANGUE Admin"
admin.site.index_title = "Painel de Administração do LANGUE"

# Customizar a aparência das listas
class CustomAdminMixin:
    """Mixin para customizar a aparência do admin"""
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)


# Aplicar o mixin aos admins se necessário
LinhaPesquisaAdmin.__bases__ = (CustomAdminMixin,) + LinhaPesquisaAdmin.__bases__
PesquisadorAdmin.__bases__ = (CustomAdminMixin,) + PesquisadorAdmin.__bases__
EstudanteAdmin.__bases__ = (CustomAdminMixin,) + EstudanteAdmin.__bases__

