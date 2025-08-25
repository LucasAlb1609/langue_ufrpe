from django.contrib import admin
from .models import Album, Foto

class FotoInline(admin.TabularInline):
    """
    Permite adicionar fotos diretamente na página de edição do Álbum.
    """
    model = Foto
    extra = 3  # Quantidade de campos extras para upload de fotos
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview', 'caption')

    def image_preview(self, obj):
        # Exibe uma miniatura da imagem no admin
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return "(Nenhuma imagem)"
    image_preview.short_description = "Pré-visualização"

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Album.
    """
    list_display = ('title', 'event_date', 'photo_count', 'created_at')
    list_filter = ('event_date',)
    search_fields = ('title', 'description')
    inlines = [FotoInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'event_date', 'cover_image')
        }),
    )

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Foto (gerenciamento individual).
    """
    list_display = ('id', 'album', 'caption', 'uploaded_at', 'image_preview')
    list_filter = ('album', 'uploaded_at')
    search_fields = ('caption', 'album__title')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return "(Nenhuma imagem)"
    image_preview.short_description = "Pré-visualização"
