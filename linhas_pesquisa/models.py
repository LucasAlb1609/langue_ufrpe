from django.db import models
from django.urls import reverse


class Pesquisador(models.Model):
    """Modelo para representar pesquisadores"""
    nome = models.CharField(max_length=200, verbose_name="Nome do Pesquisador")
    universidade = models.CharField(max_length=200, verbose_name="Universidade")
    link_lattes = models.URLField(verbose_name="Link do Currículo Lattes", blank=True, null=True)
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    class Meta:
        verbose_name = "Pesquisador"
        verbose_name_plural = "Pesquisadores"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.universidade})"


class Estudante(models.Model):
    """Modelo para representar estudantes"""
    NIVEL_CHOICES = [
        ('IC', 'Iniciação Científica'),
        ('PAVI', 'PAVI'),
        ('MESTRADO', 'Mestrado'),
        ('DOUTORADO', 'Doutorado'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name="Nome do Estudante")
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, verbose_name="Nível")
    universidade = models.CharField(max_length=200, verbose_name="Universidade")
    programa = models.CharField(max_length=200, verbose_name="Programa", blank=True, null=True)
    link_lattes = models.URLField(verbose_name="Link do Currículo Lattes", blank=True, null=True)
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    class Meta:
        verbose_name = "Estudante"
        verbose_name_plural = "Estudantes"
        ordering = ['nivel', 'nome']
    
    def __str__(self):
        return f"{self.nome} - {self.get_nivel_display()} ({self.universidade})"


class LinhaPesquisa(models.Model):
    """Modelo para representar linhas de pesquisa"""
    titulo = models.CharField(max_length=300, verbose_name="Título da Linha de Pesquisa")
    objetivo = models.TextField(verbose_name="Objetivo")
    palavras_chave = models.TextField(verbose_name="Palavras-chave", 
                                     help_text="Separe as palavras-chave por ponto e vírgula (;)")
    setores_aplicacao = models.TextField(verbose_name="Setores de Aplicação")
    imagem = models.ImageField(upload_to='linhas_pesquisa/', verbose_name="Imagem", 
                              blank=True, null=True,
                              help_text="Imagem ilustrativa da linha de pesquisa")
    
    # Relacionamentos
    pesquisadores = models.ManyToManyField(Pesquisador, 
                                         verbose_name="Pesquisadores Relacionados",
                                         blank=True)
    estudantes = models.ManyToManyField(Estudante, 
                                       verbose_name="Estudantes Relacionados",
                                       blank=True)
    
    # Campos de controle
    ativa = models.BooleanField(default=True, verbose_name="Linha Ativa")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição",
                                       help_text="Ordem em que a linha aparecerá na página")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    
    class Meta:
        verbose_name = "Linha de Pesquisa"
        verbose_name_plural = "Linhas de Pesquisa"
        ordering = ['ordem', 'titulo']
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('linhas_pesquisa_detail', kwargs={'pk': self.pk})
    
    def get_palavras_chave_list(self):
        """Retorna lista de palavras-chave"""
        if self.palavras_chave:
            return [palavra.strip() for palavra in self.palavras_chave.split(';') if palavra.strip()]
        return []
    
    def get_pesquisadores_coordenadores(self):
        """Retorna pesquisadores que são coordenadores"""
        # Assumindo que coordenadores são identificados por algum critério
        # Por simplicidade, vamos considerar que o primeiro pesquisador é o coordenador
        return self.pesquisadores.filter(ativo=True).first()
    
    def get_pesquisadores_nao_coordenadores(self):
        """Retorna pesquisadores que não são coordenadores"""
        coordenador = self.get_pesquisadores_coordenadores()
        if coordenador:
            return self.pesquisadores.filter(ativo=True).exclude(pk=coordenador.pk)
        return self.pesquisadores.filter(ativo=True)
    
    def get_estudantes_por_nivel(self):
        """Retorna estudantes agrupados por nível"""
        estudantes_dict = {}
        for estudante in self.estudantes.filter(ativo=True):
            nivel = estudante.get_nivel_display()
            if nivel not in estudantes_dict:
                estudantes_dict[nivel] = []
            estudantes_dict[nivel].append(estudante)
        return estudantes_dict


class ConfiguracaoPagina(models.Model):
    """Modelo para configurações gerais da página de linhas de pesquisa"""
    titulo_pagina = models.CharField(max_length=200, default="Linhas de Pesquisa", 
                                   verbose_name="Título da Página")
    descricao_pagina = models.TextField(verbose_name="Descrição da Página", blank=True, null=True,
                                       help_text="Texto introdutório da página")
    imagem_hero = models.ImageField(upload_to='configuracao/', verbose_name="Imagem Hero", 
                                   blank=True, null=True,
                                   help_text="Imagem de fundo da seção hero")
    
    class Meta:
        verbose_name = "Configuração da Página"
        verbose_name_plural = "Configurações da Página"
    
    def __str__(self):
        return self.titulo_pagina
    
    def save(self, *args, **kwargs):
        # Garantir que só existe uma configuração
        if not self.pk and ConfiguracaoPagina.objects.exists():
            raise ValueError('Só pode existir uma configuração de página')
        return super().save(*args, **kwargs)

