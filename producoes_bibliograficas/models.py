from django.db import models
from django.urls import reverse


class Autor(models.Model):
    """Modelo para representar autores de produções bibliográficas"""
    nome = models.CharField(max_length=200, unique=True, verbose_name="Nome Completo")
    lattes_link = models.URLField(blank=True, null=True, verbose_name="Link para Currículo Lattes")
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ["nome"]
        
    def __str__(self):
        return self.nome


class ProducaoBibliografica(models.Model):
    """Modelo para representar uma produção bibliográfica"""
    TIPO_CHOICES = [
        ("ARTIGO", "Artigo de Periódico"),
        ("LIVRO", "Livro"),
        ("CAPITULO", "Capítulo de Livro"),
        ("ANAIS", "Trabalho em Anais de Evento"),
        ("TESE", "Tese"),
        ("DISSERTACAO", "Dissertação"),
        ("OUTRO", "Outro")
    ]
    
    autores = models.ManyToManyField(Autor, related_name="producoes", verbose_name="Autores")
    titulo = models.CharField(max_length=500, verbose_name="Título da Produção")
    link_producao = models.URLField(blank=True, null=True, verbose_name="Link para a Produção")
    
    # Detalhes da publicação
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="ARTIGO", verbose_name="Tipo de Produção")
    local_publicacao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Local de Publicação (Revista, Livro, Anais)")
    volume = models.CharField(max_length=50, blank=True, null=True, verbose_name="Volume")
    numero = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número/Edição")
    paginas = models.CharField(max_length=50, blank=True, null=True, verbose_name="Páginas (ex: 628-653)")
    
    ano_publicacao = models.IntegerField(verbose_name="Ano de Publicação")
    
    # Campos de controle
    ativa = models.BooleanField(default=True, verbose_name="Ativa")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    
    class Meta:
        verbose_name = "Produção Bibliográfica"
        verbose_name_plural = "Produções Bibliográficas"
        ordering = ["-ano_publicacao", "titulo"]
        
    def __str__(self):
        autores_str = ", ".join([a.nome for a in self.autores.all()])
        return f"{autores_str} ({self.ano_publicacao}) {self.titulo}"
        
    def get_autores_display(self):
        """Retorna a string formatada dos autores"""
        return "; ".join([a.nome for a in self.autores.all()])


class ConfiguracaoPaginaProducoes(models.Model):
    """Modelo para configurações gerais da página de produções bibliográficas"""
    titulo_pagina = models.CharField(max_length=200, default="Produções Bibliográficas", 
                                   verbose_name="Título da Página")
    descricao_pagina = models.TextField(verbose_name="Descrição da Página", blank=True, null=True,
                                       help_text="Texto introdutório da página de produções bibliográficas")
    imagem_hero = models.ImageField(upload_to='configuracao_producoes/', verbose_name="Imagem Hero", 
                                   blank=True, null=True,
                                   help_text="Imagem de fundo da seção hero da página de produções")
    
    class Meta:
        verbose_name = "Configuração da Página de Produções"
        verbose_name_plural = "Configurações da Página de Produções"
    
    def __str__(self):
        return self.titulo_pagina
    
    def save(self, *args, **kwargs):
        # Garantir que só existe uma configuração
        if not self.pk and ConfiguracaoPaginaProducoes.objects.exists():
            raise ValueError('Só pode existir uma configuração de página de produções')
        return super().save(*args, **kwargs)


