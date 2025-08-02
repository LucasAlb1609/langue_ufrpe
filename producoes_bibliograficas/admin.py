from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import ProducaoBibliografica, Autor, ConfiguracaoPaginaProducoes


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'lattes_link_display', 'total_producoes']
    search_fields = ['nome']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações do Autor', {
            'fields': ('nome', 'lattes_link')
        }),
    )
    
    def lattes_link_display(self, obj):
        if obj.lattes_link:
            return format_html(
                '<a href="{}" target="_blank">Ver Lattes</a>',
                obj.lattes_link
            )
        return "Não informado"
    lattes_link_display.short_description = "Currículo Lattes"
    
    def total_producoes(self, obj):
        return obj.producoes.filter(ativa=True).count()
    total_producoes.short_description = "Total de Produções"


class AutorInline(admin.TabularInline):
    model = ProducaoBibliografica.autores.through
    extra = 1
    verbose_name = "Autor"
    verbose_name_plural = "Autores"


@admin.register(ProducaoBibliografica)
class ProducaoBibliograficaAdmin(admin.ModelAdmin):
    list_display = ['titulo_resumido', 'get_autores_display', 'tipo', 'ano_publicacao', 'local_publicacao', 'ativa']
    list_filter = ['tipo', 'ano_publicacao', 'ativa', 'data_criacao']
    search_fields = ['titulo', 'autores__nome', 'local_publicacao']
    list_editable = ['ativa']
    ordering = ['-ano_publicacao', 'titulo']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'autores', 'tipo', 'ano_publicacao')
        }),
        ('Detalhes da Publicação', {
            'fields': ('local_publicacao', 'volume', 'numero', 'paginas')
        }),
        ('Link e Configurações', {
            'fields': ('link_producao', 'ativa')
        }),
    )
    
    filter_horizontal = ['autores']
    
    readonly_fields = ['data_criacao', 'data_atualizacao']
    
    def titulo_resumido(self, obj):
        if len(obj.titulo) > 50:
            return obj.titulo[:50] + "..."
        return obj.titulo
    titulo_resumido.short_description = "Título"
    
    def get_autores_display(self, obj):
        autores = obj.autores.all()[:3]  # Mostrar apenas os 3 primeiros
        nomes = [a.nome for a in autores]
        if obj.autores.count() > 3:
            nomes.append(f"... (+{obj.autores.count() - 3})")
        return "; ".join(nomes)
    get_autores_display.short_description = "Autores"
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Customizar help_text
        if 'titulo' in form.base_fields:
            form.base_fields['titulo'].help_text = (
                "Digite o título completo da produção bibliográfica."
            )
        
        if 'paginas' in form.base_fields:
            form.base_fields['paginas'].help_text = (
                "Exemplo: 628-653 ou p. 15-30"
            )
        
        return form
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Log da ação
        if change:
            self.message_user(request, f'Produção "{obj.titulo}" atualizada com sucesso.')
        else:
            self.message_user(request, f'Produção "{obj.titulo}" criada com sucesso.')


@admin.register(ConfiguracaoPaginaProducoes)
class ConfiguracaoPaginaProducoesAdmin(admin.ModelAdmin):
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
        return not ConfiguracaoPaginaProducoes.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Não permitir deletar a configuração
        return False


# Customização adicional do admin site para produções bibliográficas
class ProducoesBibliograficasAdminMixin:
    """Mixin para customizar a aparência do admin de produções"""
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin_producoes.css',)
        }
        js = ('admin/js/custom_admin_producoes.js',)


# Aplicar o mixin aos admins se necessário
ProducaoBibliograficaAdmin.__bases__ = (ProducoesBibliograficasAdminMixin,) + ProducaoBibliograficaAdmin.__bases__
AutorAdmin.__bases__ = (ProducoesBibliograficasAdminMixin,) + AutorAdmin.__bases__


# Ações personalizadas
@admin.action(description='Marcar produções selecionadas como ativas')
def marcar_como_ativas(modeladmin, request, queryset):
    queryset.update(ativa=True)


@admin.action(description='Marcar produções selecionadas como inativas')
def marcar_como_inativas(modeladmin, request, queryset):
    queryset.update(ativa=False)


# Adicionar ações ao admin de produções
ProducaoBibliograficaAdmin.actions = [marcar_como_ativas, marcar_como_inativas]

