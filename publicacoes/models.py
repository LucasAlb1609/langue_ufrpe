from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image
import fitz  # PyMuPDF
import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from django.urls import reverse


def validate_pdf_file(file):
    """Valida se o arquivo é um PDF válido"""
    if not file.name.endswith('.pdf'):
        raise ValidationError('Apenas arquivos PDF são permitidos.')
    
    # Verifica o tamanho do arquivo (máximo 50MB)
    if file.size > 50 * 1024 * 1024:
        raise ValidationError('O arquivo PDF não pode exceder 50MB.')


def upload_pdf_path(instance, filename):
    """Define o caminho de upload para os PDFs"""
    return f'publicacoes/pdfs/{filename}'


def upload_thumbnail_path(instance, filename):
    """Define o caminho de upload para as miniaturas"""
    return f'publicacoes/thumbnails/{filename}'


class Organizador(models.Model):
    """Modelo para representar os organizadores das publicações"""
    nome = models.CharField(
        max_length=200,
        verbose_name="Nome do Organizador",
        help_text="Nome completo do organizador da publicação"
    )
    
    biografia = models.TextField(
        blank=True,
        null=True,
        verbose_name="Biografia",
        help_text="Breve biografia do organizador (opcional)"
    )
    
    lattes_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Link do Lattes",
        help_text="URL do currículo Lattes do organizador (opcional)"
    )
    
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="E-mail",
        help_text="E-mail de contato do organizador (opcional)"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Indica se o organizador está ativo no sistema"
    )
    
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    class Meta:
        verbose_name = "Organizador"
        verbose_name_plural = "Organizadores"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class PublicacaoPDF(models.Model):
    """Modelo para representar as publicações em PDF"""
    
    CATEGORIA_CHOICES = [
        ('LIVRO', 'Livro'),
        ('REVISTA', 'Revista'),
        ('ANAIS', 'Anais de Evento'),
        ('RELATORIO', 'Relatório'),
        ('MANUAL', 'Manual'),
        ('GUIA', 'Guia'),
        ('OUTROS', 'Outros'),
    ]
    
    titulo = models.CharField(
        max_length=300,
        verbose_name="Título da Publicação",
        help_text="Título completo da publicação"
    )
    
    subtitulo = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Subtítulo",
        help_text="Subtítulo da publicação (opcional)"
    )
    
    organizadores = models.ManyToManyField(
        Organizador,
        verbose_name="Organizadores",
        help_text="Selecione os organizadores desta publicação",
        related_name="publicacoes"
    )
    
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='LIVRO',
        verbose_name="Categoria",
        help_text="Categoria da publicação"
    )
    
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição",
        help_text="Breve descrição ou resumo da publicação (opcional)"
    )
    
    ano_publicacao = models.PositiveIntegerField(
        verbose_name="Ano de Publicação",
        help_text="Ano em que a publicação foi lançada"
    )
    
    editora = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Editora",
        help_text="Nome da editora responsável pela publicação (opcional)"
    )
    
    isbn = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="ISBN",
        help_text="Número ISBN da publicação (opcional)"
    )
    
    numero_paginas = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Número de Páginas",
        help_text="Total de páginas da publicação (opcional)"
    )
    
    arquivo_pdf = models.FileField(
        upload_to=upload_pdf_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            validate_pdf_file
        ],
        verbose_name="Arquivo PDF",
        help_text="Arquivo PDF da publicação (máximo 50MB)"
    )
    
    thumbnail = models.ImageField(
        upload_to=upload_thumbnail_path,
        blank=True,
        null=True,
        verbose_name="Miniatura",
        help_text="Miniatura da primeira página (gerada automaticamente)"
    )
    
    destaque = models.BooleanField(
        default=False,
        verbose_name="Publicação em Destaque",
        help_text="Marque para destacar esta publicação na página principal"
    )
    
    ativa = models.BooleanField(
        default=True,
        verbose_name="Ativa",
        help_text="Indica se a publicação está visível no site"
    )
    
    downloads = models.PositiveIntegerField(
        default=0,
        verbose_name="Downloads",
        help_text="Contador de downloads da publicação"
    )
    
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    class Meta:
        verbose_name = "Publicação PDF"
        verbose_name_plural = "Publicações PDF"
        ordering = ['-ano_publicacao', '-criado_em']
        indexes = [
            models.Index(fields=['ano_publicacao']),
            models.Index(fields=['categoria']),
            models.Index(fields=['ativa']),
            models.Index(fields=['destaque']),
        ]
    
    def __str__(self):
        return f"{self.titulo} ({self.ano_publicacao})"
    
    def save(self, *args, **kwargs):
        """Override do save para gerar thumbnail automaticamente"""
        gerar_thumb_depois = False
        if not self.pk: # Se é um novo objeto
            gerar_thumb_depois = True
        
        super().save(*args, **kwargs)
        
        # Gera thumbnail se for um novo objeto, tiver PDF e não tiver thumbnail
        if gerar_thumb_depois and self.arquivo_pdf and not self.thumbnail:
            self.gerar_thumbnail()

    def gerar_thumbnail(self):
        """Gera thumbnail da primeira página do PDF"""
        try:
            pdf_path = self.arquivo_pdf.path
            pdf_document = fitz.open(pdf_path)
            
            first_page = pdf_document[0]
            
            mat = fitz.Matrix(2.0, 2.0)
            pix = first_page.get_pixmap(matrix=mat)
            
            img_data = pix.tobytes("png")
            img = Image.open(BytesIO(img_data))
            
            img.thumbnail((400, 600), Image.Resampling.LANCZOS)
            
            buffer = BytesIO()
            img.save(buffer, format='PNG', optimize=True, quality=85)
            buffer.seek(0)
            
            thumbnail_name = f"thumb_{os.path.splitext(os.path.basename(self.arquivo_pdf.name))[0]}.png"
            
            self.thumbnail.save(
                thumbnail_name,
                ContentFile(buffer.getvalue()),
                save=False
            )
            
            super().save(update_fields=['thumbnail'])
            
            pdf_document.close()
            
        except Exception as e:
            print(f"Erro ao gerar thumbnail para {self.titulo}: {str(e)}")
    
    def get_organizadores_display(self):
        """Retorna string formatada com os nomes dos organizadores de forma segura."""
        # Primeiro, converte o QuerySet para uma lista. Isso permite usar índices negativos.
        organizadores_lista = list(self.organizadores.filter(ativo=True))
        count = len(organizadores_lista)

        if count == 0:
            return "Sem organizadores"
        elif count == 1:
            return organizadores_lista[0].nome
        elif count == 2:
            # Acessando a lista, não o queryset
            return f"{organizadores_lista[0].nome} e {organizadores_lista[1].nome}"
        else:
            # O fatiamento e a indexação agora são feitos na lista, o que é seguro
            nomes_iniciais = [org.nome for org in organizadores_lista[:-1]]
            ultimo_nome = organizadores_lista[-1].nome
            return f"{', '.join(nomes_iniciais)} e {ultimo_nome}"

    def incrementar_download(self):
        """Incrementa o contador de downloads"""
        self.downloads += 1
        self.save(update_fields=['downloads'])
    
    @property
    def titulo_completo(self):
        """Retorna título completo com subtítulo se existir"""
        if self.subtitulo:
            return f"{self.titulo}: {self.subtitulo}"
        return self.titulo
    
    @property
    def tamanho_arquivo_mb(self):
        """Retorna o tamanho do arquivo em MB"""
        if self.arquivo_pdf:
            try:
                return round(self.arquivo_pdf.size / (1024 * 1024), 2)
            except FileNotFoundError:
                return 0
        return 0
    
    def get_absolute_url(self):
        return reverse('publicacoes:detalhes', args=[str(self.id)])


class ConfiguracaoPaginaPublicacoes(models.Model):
    """Modelo para configurações gerais da página de publicações"""
    titulo_pagina = models.CharField(
        max_length=200,
        default="Publicações",
        verbose_name="Título da Página",
        help_text="Título principal exibido na página de publicações"
    )
    
    descricao_pagina = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição da Página",
        help_text="Texto descritivo exibido abaixo do título (opcional)"
    )
    
    imagem_hero = models.ImageField(
        upload_to='publicacoes/hero/',
        blank=True,
        null=True,
        verbose_name="Imagem Hero",
        help_text="Imagem de destaque para a seção hero da página (opcional)"
    )
    
    publicacoes_por_pagina = models.PositiveIntegerField(
        default=12,
        verbose_name="Publicações por Página",
        help_text="Número de publicações exibidas por página"
    )
    
    mostrar_estatisticas = models.BooleanField(
        default=True,
        verbose_name="Mostrar Estatísticas",
        help_text="Exibir seção de estatísticas na página"
    )
    
    ativa = models.BooleanField(
        default=True,
        verbose_name="Configuração Ativa",
        help_text="Indica se esta configuração está ativa"
    )
    
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    class Meta:
        verbose_name = "Configuração da Página de Publicações"
        verbose_name_plural = "Configurações da Página de Publicações"
    
    def __str__(self):
        return f"Configuração: {self.titulo_pagina}"
    
    def save(self, *args, **kwargs):
        """Garante que apenas uma configuração esteja ativa"""
        if self.ativa:
            # Exclui o objeto atual da consulta para evitar problemas em updates
            ConfiguracaoPaginaPublicacoes.objects.exclude(pk=self.pk).filter(ativa=True).update(ativa=False)
        super().save(*args, **kwargs)