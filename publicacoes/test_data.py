"""
Script para gerar dados de teste para a aplicação de Publicações PDF
Execute este script no Django shell: python manage.py shell
Depois execute: exec(open('publicacoes/test_data.py').read())
"""

import os
import random
from datetime import datetime, timedelta
from django.core.files.base import ContentFile
from django.conf import settings
from publicacoes.models import Organizador, PublicacaoPDF, ConfiguracaoPaginaPublicacoes

def criar_dados_teste():
    """Cria dados de teste para a aplicação de publicações"""
    
    print("🚀 Iniciando criação de dados de teste para Publicações PDF...")
    
    # Limpar dados existentes (opcional - descomente se quiser limpar)
    # print("🧹 Limpando dados existentes...")
    # PublicacaoPDF.objects.all().delete()
    # Organizador.objects.all().delete()
    # ConfiguracaoPaginaPublicacoes.objects.all().delete()
    
    # 1. Criar configuração da página
    print("📄 Criando configuração da página...")
    configuracao, created = ConfiguracaoPaginaPublicacoes.objects.get_or_create(
        ativa=True,
        defaults={
            'titulo_pagina': 'Publicações LANGUE UFRPE',
            'descricao_pagina': 'Explore nossa coleção de publicações acadêmicas em PDF, incluindo livros, artigos, relatórios e outros materiais de pesquisa do Laboratório de Estudos da Linguagem, Literatura e História.',
            'publicacoes_por_pagina': 12,
            'mostrar_estatisticas': True,
        }
    )
    
    if created:
        print("✅ Configuração da página criada com sucesso!")
    else:
        print("ℹ️ Configuração da página já existe.")
    
    # 2. Criar organizadores
    print("👥 Criando organizadores...")
    
    organizadores_data = [
        {
            'nome': 'Dr. João Silva Santos',
            'biografia': 'Doutor em Linguística pela UFPE, especialista em análise do discurso e sociolinguística.',
            'lattes_link': 'http://lattes.cnpq.br/1234567890123456',
            'email': 'joao.santos@ufrpe.edu.br'
        },
        {
            'nome': 'Dra. Maria Fernanda Oliveira',
            'biografia': 'Doutora em Literatura Brasileira pela USP, pesquisadora em literatura contemporânea.',
            'lattes_link': 'http://lattes.cnpq.br/2345678901234567',
            'email': 'maria.oliveira@ufrpe.edu.br'
        },
        {
            'nome': 'Dr. Carlos Eduardo Mendes',
            'biografia': 'Doutor em História pela UFMG, especialista em história do Brasil colonial.',
            'lattes_link': 'http://lattes.cnpq.br/3456789012345678',
            'email': 'carlos.mendes@ufrpe.edu.br'
        },
        {
            'nome': 'Dra. Ana Paula Costa',
            'biografia': 'Doutora em Letras pela UFRJ, pesquisadora em linguística aplicada.',
            'lattes_link': 'http://lattes.cnpq.br/4567890123456789',
            'email': 'ana.costa@ufrpe.edu.br'
        },
        {
            'nome': 'Dr. Roberto Lima Ferreira',
            'biografia': 'Doutor em Educação pela UNICAMP, especialista em ensino de língua portuguesa.',
            'lattes_link': 'http://lattes.cnpq.br/5678901234567890',
            'email': 'roberto.ferreira@ufrpe.edu.br'
        },
        {
            'nome': 'Dra. Luciana Barbosa Alves',
            'biografia': 'Doutora em Comunicação pela UFRGS, pesquisadora em mídia e sociedade.',
            'lattes_link': 'http://lattes.cnpq.br/6789012345678901',
            'email': 'luciana.alves@ufrpe.edu.br'
        },
        {
            'nome': 'Dr. Fernando Augusto Rocha',
            'biografia': 'Doutor em Filosofia pela PUC-SP, especialista em filosofia da linguagem.',
            'lattes_link': 'http://lattes.cnpq.br/7890123456789012',
            'email': 'fernando.rocha@ufrpe.edu.br'
        },
        {
            'nome': 'Dra. Patrícia Gomes Nascimento',
            'biografia': 'Doutora em Antropologia pela UnB, pesquisadora em cultura popular.',
            'lattes_link': 'http://lattes.cnpq.br/8901234567890123',
            'email': 'patricia.nascimento@ufrpe.edu.br'
        }
    ]
    
    organizadores_criados = []
    for org_data in organizadores_data:
        organizador, created = Organizador.objects.get_or_create(
            nome=org_data['nome'],
            defaults=org_data
        )
        organizadores_criados.append(organizador)
        if created:
            print(f"✅ Organizador criado: {organizador.nome}")
        else:
            print(f"ℹ️ Organizador já existe: {organizador.nome}")
    
    # 3. Criar publicações
    print("📚 Criando publicações...")
    
    publicacoes_data = [
        {
            'titulo': 'Análise do Discurso Político no Brasil Contemporâneo',
            'subtitulo': 'Uma Abordagem Sociolinguística',
            'categoria': 'LIVRO',
            'descricao': 'Este livro apresenta uma análise abrangente do discurso político brasileiro contemporâneo, utilizando ferramentas da sociolinguística para compreender as estratégias discursivas empregadas por diferentes atores políticos.',
            'ano_publicacao': 2024,
            'editora': 'Editora Universitária UFRPE',
            'isbn': '978-85-7946-123-4',
            'numero_paginas': 280,
            'destaque': True,
            'downloads': random.randint(50, 200)
        },
        {
            'titulo': 'Literatura e Identidade Regional',
            'subtitulo': 'Narrativas do Nordeste Brasileiro',
            'categoria': 'LIVRO',
            'descricao': 'Uma coletânea de ensaios sobre a literatura nordestina e sua contribuição para a formação da identidade regional brasileira.',
            'ano_publicacao': 2023,
            'editora': 'Editora Massangana',
            'isbn': '978-85-7946-124-1',
            'numero_paginas': 320,
            'destaque': True,
            'downloads': random.randint(30, 150)
        },
        {
            'titulo': 'História Oral e Memória Coletiva',
            'categoria': 'REVISTA',
            'descricao': 'Artigo publicado na Revista de História da UFRPE sobre metodologias de história oral e sua importância para a preservação da memória coletiva.',
            'ano_publicacao': 2023,
            'editora': 'Revista de História UFRPE',
            'numero_paginas': 25,
            'downloads': random.randint(20, 80)
        },
        {
            'titulo': 'Ensino de Língua Portuguesa na Era Digital',
            'subtitulo': 'Desafios e Oportunidades',
            'categoria': 'MANUAL',
            'descricao': 'Manual prático para professores sobre como integrar tecnologias digitais no ensino de língua portuguesa.',
            'ano_publicacao': 2024,
            'editora': 'UFRPE Press',
            'numero_paginas': 150,
            'downloads': random.randint(40, 120)
        },
        {
            'titulo': 'Anais do III Simpósio de Linguística Aplicada',
            'categoria': 'ANAIS',
            'descricao': 'Coletânea de trabalhos apresentados no III Simpósio de Linguística Aplicada da UFRPE, abordando temas contemporâneos da área.',
            'ano_publicacao': 2023,
            'editora': 'UFRPE',
            'numero_paginas': 450,
            'downloads': random.randint(60, 180)
        },
        {
            'titulo': 'Relatório de Pesquisa: Variação Linguística no Agreste Pernambucano',
            'categoria': 'RELATORIO',
            'descricao': 'Relatório final da pesquisa sobre variação linguística realizada em comunidades rurais do agreste pernambucano.',
            'ano_publicacao': 2022,
            'numero_paginas': 95,
            'downloads': random.randint(15, 60)
        },
        {
            'titulo': 'Guia de Redação Acadêmica',
            'subtitulo': 'Normas e Práticas para Trabalhos Científicos',
            'categoria': 'GUIA',
            'descricao': 'Guia completo para elaboração de trabalhos acadêmicos, incluindo normas ABNT e técnicas de escrita científica.',
            'ano_publicacao': 2024,
            'editora': 'Editora Universitária UFRPE',
            'numero_paginas': 120,
            'destaque': True,
            'downloads': random.randint(80, 250)
        },
        {
            'titulo': 'Cultura Popular e Tradições Orais',
            'categoria': 'LIVRO',
            'descricao': 'Estudo antropológico sobre as tradições orais e manifestações da cultura popular no interior de Pernambuco.',
            'ano_publicacao': 2022,
            'editora': 'Editora Massangana',
            'isbn': '978-85-7946-125-8',
            'numero_paginas': 200,
            'downloads': random.randint(25, 90)
        },
        {
            'titulo': 'Filosofia da Linguagem: Perspectivas Contemporâneas',
            'categoria': 'REVISTA',
            'descricao': 'Artigo sobre as principais correntes da filosofia da linguagem no século XXI.',
            'ano_publicacao': 2023,
            'editora': 'Revista de Filosofia UFRPE',
            'numero_paginas': 30,
            'downloads': random.randint(10, 50)
        },
        {
            'titulo': 'Mídia Digital e Transformações Sociais',
            'subtitulo': 'Impactos na Comunicação Contemporânea',
            'categoria': 'LIVRO',
            'descricao': 'Análise dos impactos das mídias digitais nas transformações sociais e comunicacionais da sociedade contemporânea.',
            'ano_publicacao': 2024,
            'editora': 'Editora Universitária UFRPE',
            'isbn': '978-85-7946-126-5',
            'numero_paginas': 240,
            'downloads': random.randint(35, 110)
        },
        {
            'titulo': 'Manual de Metodologia de Pesquisa em Humanidades',
            'categoria': 'MANUAL',
            'descricao': 'Manual abrangente sobre metodologias de pesquisa específicas para as áreas de humanidades.',
            'ano_publicacao': 2023,
            'editora': 'UFRPE Press',
            'numero_paginas': 180,
            'downloads': random.randint(45, 140)
        },
        {
            'titulo': 'Coletânea de Textos Literários Regionais',
            'categoria': 'OUTROS',
            'descricao': 'Seleção de textos literários de autores regionais, com análises críticas e contextualizações históricas.',
            'ano_publicacao': 2022,
            'editora': 'Editora Regional',
            'numero_paginas': 300,
            'downloads': random.randint(20, 75)
        }
    ]
    
    publicacoes_criadas = []
    for pub_data in publicacoes_data:
        # Criar a publicação
        publicacao, created = PublicacaoPDF.objects.get_or_create(
            titulo=pub_data['titulo'],
            defaults=pub_data
        )
        
        if created:
            # Adicionar organizadores aleatórios (1-3 organizadores por publicação)
            num_organizadores = random.randint(1, 3)
            organizadores_selecionados = random.sample(organizadores_criados, num_organizadores)
            publicacao.organizadores.set(organizadores_selecionados)
            
            publicacoes_criadas.append(publicacao)
            print(f"✅ Publicação criada: {publicacao.titulo}")
            print(f"   Organizadores: {', '.join([org.nome for org in organizadores_selecionados])}")
        else:
            publicacoes_criadas.append(publicacao)
            print(f"ℹ️ Publicação já existe: {publicacao.titulo}")
    
    # 4. Estatísticas finais
    print("\n📊 Estatísticas dos dados criados:")
    print(f"   👥 Organizadores: {Organizador.objects.count()}")
    print(f"   📚 Publicações: {PublicacaoPDF.objects.count()}")
    print(f"   ⭐ Publicações em destaque: {PublicacaoPDF.objects.filter(destaque=True).count()}")
    print(f"   📅 Anos de publicação: {PublicacaoPDF.objects.values_list('ano_publicacao', flat=True).distinct().count()}")
    
    # Estatísticas por categoria
    print("\n📈 Publicações por categoria:")
    for categoria, nome in PublicacaoPDF.CATEGORIA_CHOICES:
        count = PublicacaoPDF.objects.filter(categoria=categoria).count()
        if count > 0:
            print(f"   {nome}: {count}")
    
    print("\n🎉 Dados de teste criados com sucesso!")
    print("\n💡 Próximos passos:")
    print("   1. Execute as migrações: python manage.py makemigrations publicacoes")
    print("   2. Aplique as migrações: python manage.py migrate")
    print("   3. Acesse o admin em /admin/ para gerenciar as publicações")
    print("   4. Acesse a página em /publicacoes/ para ver o resultado")
    print("\n⚠️ Nota: Para que as miniaturas sejam geradas automaticamente,")
    print("   você precisará fazer upload de arquivos PDF reais através do admin.")

# Executar a função
if __name__ == '__main__':
    criar_dados_teste()
else:
    # Quando executado via exec() no Django shell
    criar_dados_teste()

