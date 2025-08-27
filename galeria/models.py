from django.db import models
from django.utils import timezone
from django.urls import reverse

class Album(models.Model):
    """
    Representa um álbum de fotos, como um evento ou congresso.
    """
    title = models.CharField(max_length=200, verbose_name="Título do Álbum")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    cover_image = models.ImageField(upload_to='galeria/covers/', verbose_name="Imagem de Capa")
    event_date = models.DateField(default=timezone.now, verbose_name="Data do Evento")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Álbum"
        verbose_name_plural = "Álbuns"
        ordering = ['-event_date']

    def __str__(self):
        return self.title

    def photo_count(self):
        """
        Retorna a contagem de fotos neste álbum.
        """
        return self.photos.count()

    def get_absolute_url(self):
        return reverse('galeria:detalhe', args=[str(self.id)])

class Foto(models.Model):
    """
    Representa uma única foto, que pertence a um Álbum.
    """
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE, verbose_name="Álbum")
    image = models.ImageField(upload_to='galeria/photos/', verbose_name="Imagem")
    caption = models.CharField(max_length=255, blank=True, null=True, verbose_name="Legenda")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em")

    class Meta:
        verbose_name = "Foto"
        verbose_name_plural = "Fotos"
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Foto de {self.album.title} - {self.id}"
