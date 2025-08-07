from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import PublicacaoPDF, Organizador, ConfiguracaoPaginaPublicacoes
import tempfile
import os


class OrganizadorModelTest(TestCase):
    """Testes para o modelo Organizador"""
    
    def setUp(self):
        self.organizador = Organizador.objects.create(
            nome="Dr. João Silva",
            biografia="Doutor em Linguística",
            lattes_link="http://lattes.cnpq.br/1234567890",
            email="joao@ufrpe.edu.br"
        )
    
    def test_str_representation(self):
        """Testa a representação string do organizador"""
        self.assertEqual(str(self.organizador), "Dr. João Silva")
    
    def test_organizador_creation(self):
        """Testa a criação de um organizador"""
        self.assertTrue(isinstance(self.organizador, Organizador))
        self.assertEqual(self.organizador.nome, "Dr. João Silva")
        self.assertTrue(self.organizador.ativo)


class PublicacaoPDFModelTest(TestCase):
    """Testes para o modelo PublicacaoPDF"""
    
    def setUp(self):
        self.organizador = Organizador.objects.create(
            nome="Dr. João Silva",
            email="joao@ufrpe.edu.br"
        )
        
        # Criar um arquivo PDF temporário para teste
        self.temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        self.temp_pdf.write(b'%PDF-1.4 fake pdf content')
        self.temp_pdf.close()
        
        with open(self.temp_pdf.name, 'rb') as f:
            pdf_file = SimpleUploadedFile(
                "test.pdf",
                f.read(),
                content_type="application/pdf"
            )
            
            self.publicacao = PublicacaoPDF.objects.create(
                titulo="Teste de Publicação",
                categoria="LIVRO",
                ano_publicacao=2024,
                arquivo_pdf=pdf_file
            )
            self.publicacao.organizadores.add(self.organizador)
    
    def tearDown(self):
        """Limpa arquivos temporários"""
        if os.path.exists(self.temp_pdf.name):
            os.unlink(self.temp_pdf.name)
        
        # Remove arquivo de upload se existir
        if self.publicacao.arquivo_pdf:
            if os.path.exists(self.publicacao.arquivo_pdf.path):
                os.unlink(self.publicacao.arquivo_pdf.path)
    
    def test_str_representation(self):
        """Testa a representação string da publicação"""
        expected = f"{self.publicacao.titulo} ({self.publicacao.ano_publicacao})"
        self.assertEqual(str(self.publicacao), expected)
    
    def test_publicacao_creation(self):
        """Testa a criação de uma publicação"""
        self.assertTrue(isinstance(self.publicacao, PublicacaoPDF))
        self.assertEqual(self.publicacao.titulo, "Teste de Publicação")
        self.assertEqual(self.publicacao.categoria, "LIVRO")
        self.assertTrue(self.publicacao.ativa)
    
    def test_get_organizadores_display(self):
        """Testa o método get_organizadores_display"""
        display = self.publicacao.get_organizadores_display()
        self.assertEqual(display, "Dr. João Silva")
    
    def test_titulo_completo_property(self):
        """Testa a propriedade titulo_completo"""
        self.assertEqual(self.publicacao.titulo_completo, "Teste de Publicação")
        
        # Teste com subtítulo
        self.publicacao.subtitulo = "Um Subtítulo"
        self.publicacao.save()
        self.assertEqual(
            self.publicacao.titulo_completo, 
            "Teste de Publicação: Um Subtítulo"
        )
    
    def test_incrementar_download(self):
        """Testa o método incrementar_download"""
        downloads_inicial = self.publicacao.downloads
        self.publicacao.incrementar_download()
        self.assertEqual(self.publicacao.downloads, downloads_inicial + 1)


class PublicacoesViewTest(TestCase):
    """Testes para as views da aplicação"""
    
    def setUp(self):
        self.client = Client()
        
        # Criar configuração
        self.configuracao = ConfiguracaoPaginaPublicacoes.objects.create(
            titulo_pagina="Publicações Teste",
            ativa=True
        )
        
        # Criar organizador
        self.organizador = Organizador.objects.create(
            nome="Dr. Teste",
            email="teste@ufrpe.edu.br"
        )
        
        # Criar publicação
        self.publicacao = PublicacaoPDF.objects.create(
            titulo="Publicação Teste",
            categoria="LIVRO",
            ano_publicacao=2024,
            ativa=True
        )
        self.publicacao.organizadores.add(self.organizador)
    
    def test_lista_publicacoes_view(self):
        """Testa a view de lista de publicações"""
        url = reverse('publicacoes:lista')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Publicação Teste")
        self.assertContains(response, "Dr. Teste")
    
    def test_filtro_categoria(self):
        """Testa o filtro por categoria"""
        url = reverse('publicacoes:lista')
        response = self.client.get(url, {'categoria': 'LIVRO'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Publicação Teste")
    
    def test_busca_publicacoes(self):
        """Testa a busca por publicações"""
        url = reverse('publicacoes:lista')
        response = self.client.get(url, {'busca': 'Teste'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Publicação Teste")
    
    def test_incrementar_download_ajax(self):
        """Testa o endpoint AJAX de incrementar download"""
        url = reverse('publicacoes:incrementar_download', args=[self.publicacao.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o download foi incrementado
        self.publicacao.refresh_from_db()
        self.assertEqual(self.publicacao.downloads, 1)
    
    def test_buscar_publicacoes_ajax(self):
        """Testa o endpoint AJAX de busca"""
        url = reverse('publicacoes:buscar_ajax')
        response = self.client.get(url, {'q': 'Teste'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertTrue(len(data['results']) > 0)


class ConfiguracaoPaginaTest(TestCase):
    """Testes para o modelo ConfiguracaoPaginaPublicacoes"""
    
    def test_apenas_uma_configuracao_ativa(self):
        """Testa se apenas uma configuração pode estar ativa"""
        # Criar primeira configuração
        config1 = ConfiguracaoPaginaPublicacoes.objects.create(
            titulo_pagina="Config 1",
            ativa=True
        )
        
        # Criar segunda configuração ativa
        config2 = ConfiguracaoPaginaPublicacoes.objects.create(
            titulo_pagina="Config 2",
            ativa=True
        )
        
        # Verificar se apenas a segunda está ativa
        config1.refresh_from_db()
        self.assertFalse(config1.ativa)
        self.assertTrue(config2.ativa)


class AdminTest(TestCase):
    """Testes para o painel administrativo"""
    
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        self.client.login(username='admin', password='testpass123')
        
        self.organizador = Organizador.objects.create(
            nome="Dr. Admin Teste",
            email="admin@ufrpe.edu.br"
        )
    
    def test_admin_organizador_list(self):
        """Testa a lista de organizadores no admin"""
        url = reverse('admin:publicacoes_organizador_changelist')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr. Admin Teste")
    
    def test_admin_publicacao_add(self):
        """Testa a adição de publicação no admin"""
        url = reverse('admin:publicacoes_publicacaopdf_add')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Título da Publicação")


class APITest(TestCase):
    """Testes para a API REST"""
    
    def setUp(self):
        self.organizador = Organizador.objects.create(
            nome="Dr. API Teste",
            email="api@ufrpe.edu.br"
        )
        
        self.publicacao = PublicacaoPDF.objects.create(
            titulo="API Teste Publicação",
            categoria="LIVRO",
            ano_publicacao=2024,
            ativa=True
        )
        self.publicacao.organizadores.add(self.organizador)
    
    def test_api_publicacoes_list(self):
        """Testa o endpoint de lista da API"""
        url = reverse('publicacoes:publicacaopdf-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
    
    def test_api_estatisticas(self):
        """Testa o endpoint de estatísticas da API"""
        url = reverse('publicacoes:publicacaopdf-estatisticas')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_publicacoes', data)
        self.assertIn('total_organizadores', data)

