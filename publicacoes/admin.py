from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import PublicacaoPDF, Organizador, ConfiguracaoPaginaPublicacoes


@admin.register(Organizador)
class OrganizadorAdmin(admin.ModelAdmin):
    """Configuração do admin para o modelo Organizador"""
    
    list_display = [
        'nome',
        'email',
        'tem_lattes',
        'total_publicacoes',
        'ativo',
        'criado_em'
    ]
    
    list_filter = [
        'ativo',
        'criado_em',
        'atualizado_em'
    ]
    
    search_fields = [
        'nome',
        'email',
        'biografia'
    ]
    
    list_editable = ['ativo']
    
    readonly_fields = [
        'criado_em',
        'atualizado_em',
        'total_publicacoes'
    ]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'email', 'ativo')
        }),
        ('Informações Acadêmicas', {
            'fields': ('biografia', 'lattes_link'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('total_publicacoes', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def tem_lattes(self, obj):
        """Indica se o organizador tem link do Lattes"""
        if obj.lattes_link:
            return format_html(
                '<span style="color: green;">✓ Sim</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Não</span>'
        )
    tem_lattes.short_description = 'Tem Lattes'
    
    def total_publicacoes(self, obj):
        """Retorna o total de publicações do organizador"""
        total = obj.publicacoes.filter(ativa=True).count()
        if total > 0:
            url = reverse('admin:publicacoes_publicacaopdf_changelist')
            return format_html(
                '<a href="{}?organizadores__id__exact={}">{} publicação{}</a>',
                url,
                obj.id,
                total,
                's' if total != 1 else ''
            )
        return '0 publicações'
    total_publicacoes.short_description = 'Total de Publicações'


class OrganizadorInline(admin.TabularInline):
    """Inline para organizadores nas publicações"""
    model = PublicacaoPDF.organizadores.through
    extra = 1
    verbose_name = "Organizador"
    verbose_name_plural = "Organizadores"


@admin.register(PublicacaoPDF)
class PublicacaoPDFAdmin(admin.ModelAdmin):
    """Configuração do admin para o modelo PublicacaoPDF"""
    
    list_display = [
        'titulo_truncado',
        'categoria',
        'ano_publicacao',
        'organizadores_display',
        'downloads',
        'destaque',
        'ativa',
        'preview_thumbnail'
    ]
    
    list_filter = [
        'categoria',
        'ano_publicacao',
        'destaque',
        'ativa',
        'criado_em',
        'organizadores'
    ]
    
    search_fields = [
        'titulo',
        'subtitulo',
        'descricao',
        'editora',
        'isbn',
        'organizadores__nome'
    ]
    
    list_editable = [
        'destaque',
        'ativa'
    ]
    
    readonly_fields = [
        'downloads',
        'criado_em',
        'atualizado_em',
        'preview_thumbnail_large',
        'tamanho_arquivo_mb',
        'link_download'
    ]
    
    filter_horizontal = ['organizadores']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'titulo',
                'subtitulo',
                'categoria',
                'ano_publicacao',
                'organizadores'
            )
        }),
        ('Conteúdo', {
            'fields': (
                'descricao',
                'arquivo_pdf',
                'preview_thumbnail_large'
            )
        }),
        ('Informações da Publicação', {
            'fields': (
                'editora',
                'isbn',
                'numero_paginas'
            ),
            'classes': ('collapse',)
        }),
        ('Configurações', {
            'fields': (
                'destaque',
                'ativa'
            )
        }),
        ('Estatísticas e Metadados', {
            'fields': (
                'downloads',
                'tamanho_arquivo_mb',
                'link_download',
                'criado_em',
                'atualizado_em'
            ),
            'classes': ('collapse',)
        }),
    )
    
    actions = [
        'marcar_como_destaque',
        'remover_destaque',
        'ativar_publicacoes',
        'desativar_publicacoes',
        'regenerar_thumbnails'
    ]
    
    def titulo_truncado(self, obj):
        """Retorna título truncado para a lista"""
        if len(obj.titulo) > 50:
            return f"{obj.titulo[:47]}..."
        return obj.titulo
    titulo_truncado.short_description = 'Título'
    
    def organizadores_display(self, obj):
        """Exibe os organizadores na lista"""
        organizadores = obj.organizadores.filter(ativo=True)[:3]
        if not organizadores:
            return "Sem organizadores"
        
        nomes = [org.nome for org in organizadores]
        if obj.organizadores.filter(ativo=True).count() > 3:
            nomes.append("...")
        
        return ", ".join(nomes)
    organizadores_display.short_description = 'Organizadores'
    
    def preview_thumbnail(self, obj):
        """Exibe thumbnail pequeno na lista"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 40px; height: auto; border-radius: 4px;" />',
                obj.thumbnail.url
            )
        return format_html(
            '<span style="color: #999;">Sem thumbnail</span>'
        )
    preview_thumbnail.short_description = 'Thumbnail'
    
    def preview_thumbnail_large(self, obj):
        """Exibe thumbnail grande no formulário"""
        if obj.thumbnail:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<img src="{}" style="max-width: 200px; height: auto; border: 1px solid #ddd; border-radius: 8px;" />'
                '<p style="margin-top: 5px; color: #666; font-size: 12px;">Thumbnail gerado automaticamente da primeira página do PDF</p>'
                '</div>',
                obj.thumbnail.url
            )
        return format_html(
            '<div style="margin: 10px 0; padding: 20px; background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; text-align: center;">'
            '<p style="color: #6c757d; margin: 0;">Thumbnail será gerado automaticamente após o upload do PDF</p>'
            '</div>'
        )
    preview_thumbnail_large.short_description = 'Preview do Thumbnail'
    
    def link_download(self, obj):
        """Exibe link para download do PDF"""
        if obj.arquivo_pdf:
            return format_html(
                '<a href="{}" target="_blank" style="color: #007cba; text-decoration: none;">'
                '📄 Baixar PDF ({} MB)</a>',
                obj.arquivo_pdf.url,
                obj.tamanho_arquivo_mb
            )
        return "Nenhum arquivo"
    link_download.short_description = 'Download'
    
    def marcar_como_destaque(self, request, queryset):
        """Ação para marcar publicações como destaque"""
        updated = queryset.update(destaque=True)
        self.message_user(
            request,
            f'{updated} publicação(ões) marcada(s) como destaque.'
        )
    marcar_como_destaque.short_description = "Marcar como destaque"
    
    def remover_destaque(self, request, queryset):
        """Ação para remover destaque das publicações"""
        updated = queryset.update(destaque=False)
        self.message_user(
            request,
            f'{updated} publicação(ões) removida(s) do destaque.'
        )
    remover_destaque.short_description = "Remover destaque"
    
    def ativar_publicacoes(self, request, queryset):
        """Ação para ativar publicações"""
        updated = queryset.update(ativa=True)
        self.message_user(
            request,
            f'{updated} publicação(ões) ativada(s).'
        )
    ativar_publicacoes.short_description = "Ativar publicações"
    
    def desativar_publicacoes(self, request, queryset):
        """Ação para desativar publicações"""
        updated = queryset.update(ativa=False)
        self.message_user(
            request,
            f'{updated} publicação(ões) desativada(s).'
        )
    desativar_publicacoes.short_description = "Desativar publicações"
    
    def regenerar_thumbnails(self, request, queryset):
        """Ação para regenerar thumbnails das publicações"""
        count = 0
        for publicacao in queryset:
            if publicacao.arquivo_pdf:
                try:
                    publicacao.gerar_thumbnail()
                    count += 1
                except Exception as e:
                    self.message_user(
                        request,
                        f'Erro ao regenerar thumbnail para "{publicacao.titulo}": {str(e)}',
                        level='ERROR'
                    )
        
        if count > 0:
            self.message_user(
                request,
                f'{count} thumbnail(s) regenerado(s) com sucesso.'
            )
    regenerar_thumbnails.short_description = "Regenerar thumbnails"
    
    def save_model(self, request, obj, form, change):
        """Override para gerar thumbnail após salvar"""
        super().save_model(request, obj, form, change)
        
        # Se é uma nova publicação ou o PDF foi alterado, gera thumbnail
        if not change or 'arquivo_pdf' in form.changed_data:
            if obj.arquivo_pdf:
                try:
                    obj.gerar_thumbnail()
                    self.message_user(
                        request,
                        f'Thumbnail gerado automaticamente para "{obj.titulo}".'
                    )
                except Exception as e:
                    self.message_user(
                        request,
                        f'Erro ao gerar thumbnail: {str(e)}',
                        level='ERROR'
                    )


@admin.register(ConfiguracaoPaginaPublicacoes)
class ConfiguracaoPaginaPublicacoesAdmin(admin.ModelAdmin):
    """Configuração do admin para ConfiguracaoPaginaPublicacoes"""
    
    list_display = [
        'titulo_pagina',
        'publicacoes_por_pagina',
        'mostrar_estatisticas',
        'ativa',
        'atualizado_em'
    ]
    
    list_filter = [
        'ativa',
        'mostrar_estatisticas',
        'criado_em'
    ]
    
    search_fields = [
        'titulo_pagina',
        'descricao_pagina'
    ]
    
    readonly_fields = [
        'criado_em',
        'atualizado_em'
    ]
    
    fieldsets = (
        ('Configurações da Página', {
            'fields': (
                'titulo_pagina',
                'descricao_pagina',
                'imagem_hero'
            )
        }),
        ('Configurações de Exibição', {
            'fields': (
                'publicacoes_por_pagina',
                'mostrar_estatisticas',
                'ativa'
            )
        }),
        ('Metadados', {
            'fields': (
                'criado_em',
                'atualizado_em'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Permite adicionar apenas se não houver configuração ativa"""
        return not ConfiguracaoPaginaPublicacoes.objects.filter(ativa=True).exists()
    
    def has_delete_permission(self, request, obj=None):
        """Impede deletar se for a única configuração ativa"""
        if obj and obj.ativa:
            return ConfiguracaoPaginaPublicacoes.objects.filter(ativa=True).count() > 1
        return True


# Customização do admin site
admin.site.site_header = "LANGUE UFRPE - Administração"
admin.site.site_title = "LANGUE UFRPE Admin"
admin.site.index_title = "Painel de Administração"

