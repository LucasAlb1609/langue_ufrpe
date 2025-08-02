#!/usr/bin/env python
"""
Script para gerar dados de teste para Produções Bibliográficas
Execute este script no shell do Django: python manage.py shell < producoes_bibliograficas/test_data.py
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'langue.settings')
django.setup()

from producoes_bibliograficas.models import ProducaoBibliografica, Autor, ConfiguracaoPaginaProducoes


def criar_dados_teste():
    """Cria dados de teste para produções bibliográficas"""
    
    print("🚀 Iniciando criação de dados de teste para Produções Bibliográficas...")
    
    # Criar configuração da página
    configuracao, created = ConfiguracaoPaginaProducoes.objects.get_or_create(
        defaults={
            'titulo_pagina': 'Produções Bibliográficas',
            'descricao_pagina': 'Conheça as principais produções científicas e acadêmicas do LANGUE UFRPE, incluindo artigos, livros, capítulos e trabalhos apresentados em eventos.'
        }
    )
    
    if created:
        print("✅ Configuração da página criada")
    else:
        print("ℹ️ Configuração da página já existe")
    
    # Criar autores
    autores_data = [
        {
            'nome': 'AZEVEDO, NATANAEL DUARTE DE',
            'lattes_link': 'http://lattes.cnpq.br/1234567890123456'
        },
        {
            'nome': 'FERREIRA JUNIOR, J. T.',
            'lattes_link': 'http://lattes.cnpq.br/2345678901234567'
        },
        {
            'nome': 'SILVA, MARIA JOSÉ DA',
            'lattes_link': 'http://lattes.cnpq.br/3456789012345678'
        },
        {
            'nome': 'SANTOS, JOÃO CARLOS DOS',
            'lattes_link': 'http://lattes.cnpq.br/4567890123456789'
        },
        {
            'nome': 'OLIVEIRA, ANA PAULA DE',
            'lattes_link': 'http://lattes.cnpq.br/5678901234567890'
        },
        {
            'nome': 'COSTA, PEDRO HENRIQUE',
            'lattes_link': 'http://lattes.cnpq.br/6789012345678901'
        },
        {
            'nome': 'LIMA, CARLA FERNANDA',
            'lattes_link': 'http://lattes.cnpq.br/7890123456789012'
        },
        {
            'nome': 'RODRIGUES, MARCOS ANTONIO',
            'lattes_link': 'http://lattes.cnpq.br/8901234567890123'
        }
    ]
    
    autores_criados = []
    for autor_data in autores_data:
        autor, created = Autor.objects.get_or_create(
            nome=autor_data['nome'],
            defaults={'lattes_link': autor_data['lattes_link']}
        )
        autores_criados.append(autor)
        if created:
            print(f"✅ Autor criado: {autor.nome}")
        else:
            print(f"ℹ️ Autor já existe: {autor.nome}")
    
    # Criar produções bibliográficas
    producoes_data = [
        {
            'titulo': 'Historicidade das cartas de amor: circulação de manuais epistolares portugueses no Brasil do século XIX',
            'link_producao': 'https://revista.abralin.org/index.php/abralin/article/view/1234',
            'tipo': 'ARTIGO',
            'local_publicacao': 'Revista da ABRALIN',
            'volume': '19',
            'numero': '3',
            'paginas': '628-653',
            'ano_publicacao': 2020,
            'autores_nomes': ['AZEVEDO, NATANAEL DUARTE DE', 'FERREIRA JUNIOR, J. T.']
        },
        {
            'titulo': 'Análise discursiva de textos literários do século XIX: uma abordagem linguística',
            'link_producao': 'https://periodicos.ufpe.br/revistas/estudoslinguisticos/article/view/5678',
            'tipo': 'ARTIGO',
            'local_publicacao': 'Estudos Linguísticos',
            'volume': '48',
            'numero': '2',
            'paginas': '234-256',
            'ano_publicacao': 2021,
            'autores_nomes': ['SILVA, MARIA JOSÉ DA', 'AZEVEDO, NATANAEL DUARTE DE']
        },
        {
            'titulo': 'Literatura e História: interfaces metodológicas na pesquisa acadêmica',
            'link_producao': 'https://editora.ufrpe.br/livros/literatura-historia-interfaces',
            'tipo': 'LIVRO',
            'local_publicacao': 'Editora UFRPE',
            'volume': '',
            'numero': '',
            'paginas': '1-280',
            'ano_publicacao': 2022,
            'autores_nomes': ['SANTOS, JOÃO CARLOS DOS', 'OLIVEIRA, ANA PAULA DE']
        },
        {
            'titulo': 'Metodologias de pesquisa em linguística histórica',
            'link_producao': 'https://editora.contexto.com.br/capitulo-metodologias-pesquisa',
            'tipo': 'CAPITULO',
            'local_publicacao': 'Linguística Histórica: teoria e prática',
            'volume': '',
            'numero': '',
            'paginas': '45-78',
            'ano_publicacao': 2021,
            'autores_nomes': ['COSTA, PEDRO HENRIQUE', 'LIMA, CARLA FERNANDA']
        },
        {
            'titulo': 'Variação linguística no português brasileiro: um estudo diacrônico',
            'link_producao': 'https://anais.gelne.org.br/trabalho/variacao-linguistica-portugues',
            'tipo': 'ANAIS',
            'local_publicacao': 'Anais do GELNE 2023',
            'volume': '35',
            'numero': '',
            'paginas': '156-170',
            'ano_publicacao': 2023,
            'autores_nomes': ['RODRIGUES, MARCOS ANTONIO', 'SILVA, MARIA JOSÉ DA']
        },
        {
            'titulo': 'Epistolografia feminina no Brasil oitocentista: análise de cartas pessoais',
            'link_producao': 'https://repositorio.ufrpe.br/tese/epistolografia-feminina-brasil',
            'tipo': 'TESE',
            'local_publicacao': 'Programa de Pós-Graduação em Letras - UFRPE',
            'volume': '',
            'numero': '',
            'paginas': '1-350',
            'ano_publicacao': 2020,
            'autores_nomes': ['LIMA, CARLA FERNANDA']
        },
        {
            'titulo': 'Aspectos morfossintáticos do português arcaico: uma análise de documentos medievais',
            'link_producao': 'https://repositorio.ufrpe.br/dissertacao/aspectos-morfossintaticos',
            'tipo': 'DISSERTACAO',
            'local_publicacao': 'Programa de Pós-Graduação em Letras - UFRPE',
            'volume': '',
            'numero': '',
            'paginas': '1-180',
            'ano_publicacao': 2019,
            'autores_nomes': ['COSTA, PEDRO HENRIQUE']
        },
        {
            'titulo': 'Tradições discursivas em cartas comerciais do século XVIII',
            'link_producao': 'https://revista.filologia.org.br/artigo/tradicoes-discursivas-cartas',
            'tipo': 'ARTIGO',
            'local_publicacao': 'Revista de Filologia e Linguística Portuguesa',
            'volume': '22',
            'numero': '1',
            'paginas': '89-112',
            'ano_publicacao': 2022,
            'autores_nomes': ['AZEVEDO, NATANAEL DUARTE DE', 'SANTOS, JOÃO CARLOS DOS']
        },
        {
            'titulo': 'O papel da mulher na literatura brasileira do século XIX',
            'link_producao': 'https://editora.mulheres.com.br/capitulo-papel-mulher-literatura',
            'tipo': 'CAPITULO',
            'local_publicacao': 'Mulheres na Literatura Brasileira',
            'volume': '',
            'numero': '',
            'paginas': '123-145',
            'ano_publicacao': 2023,
            'autores_nomes': ['OLIVEIRA, ANA PAULA DE', 'LIMA, CARLA FERNANDA']
        },
        {
            'titulo': 'Linguagem e poder nas correspondências oficiais do período colonial',
            'link_producao': 'https://anais.anpoll.org.br/trabalho/linguagem-poder-correspondencias',
            'tipo': 'ANAIS',
            'local_publicacao': 'Anais da ANPOLL 2022',
            'volume': '33',
            'numero': '',
            'paginas': '445-460',
            'ano_publicacao': 2022,
            'autores_nomes': ['FERREIRA JUNIOR, J. T.', 'RODRIGUES, MARCOS ANTONIO']
        },
        {
            'titulo': 'Dicionário de termos linguísticos do português histórico',
            'link_producao': 'https://editora.ufrpe.br/dicionarios/termos-linguisticos-historico',
            'tipo': 'LIVRO',
            'local_publicacao': 'Editora UFRPE',
            'volume': '',
            'numero': '',
            'paginas': '1-450',
            'ano_publicacao': 2023,
            'autores_nomes': ['SILVA, MARIA JOSÉ DA', 'COSTA, PEDRO HENRIQUE', 'AZEVEDO, NATANAEL DUARTE DE']
        },
        {
            'titulo': 'Análise paleográfica de manuscritos brasileiros dos séculos XVII e XVIII',
            'link_producao': 'https://revista.paleografia.org.br/artigo/analise-paleografica-manuscritos',
            'tipo': 'ARTIGO',
            'local_publicacao': 'Revista Brasileira de Paleografia',
            'volume': '15',
            'numero': '2',
            'paginas': '78-95',
            'ano_publicacao': 2021,
            'autores_nomes': ['SANTOS, JOÃO CARLOS DOS']
        },
        {
            'titulo': 'Edição crítica de cartas jesuíticas do século XVI',
            'link_producao': 'https://editora.jesuitica.org.br/edicao-critica-cartas',
            'tipo': 'LIVRO',
            'local_publicacao': 'Editora Jesuítica',
            'volume': '',
            'numero': '',
            'paginas': '1-320',
            'ano_publicacao': 2019,
            'autores_nomes': ['RODRIGUES, MARCOS ANTONIO', 'OLIVEIRA, ANA PAULA DE']
        },
        {
            'titulo': 'Sociolinguística histórica: métodos e aplicações',
            'link_producao': 'https://anais.abralin.org.br/trabalho/sociolinguistica-historica-metodos',
            'tipo': 'ANAIS',
            'local_publicacao': 'Anais da ABRALIN 2020',
            'volume': '31',
            'numero': '',
            'paginas': '234-248',
            'ano_publicacao': 2020,
            'autores_nomes': ['LIMA, CARLA FERNANDA', 'FERREIRA JUNIOR, J. T.']
        },
        {
            'titulo': 'Gramática histórica do português brasileiro: uma perspectiva funcional',
            'link_producao': 'https://repositorio.ufrpe.br/dissertacao/gramatica-historica-portugues',
            'tipo': 'DISSERTACAO',
            'local_publicacao': 'Programa de Pós-Graduação em Letras - UFRPE',
            'volume': '',
            'numero': '',
            'paginas': '1-220',
            'ano_publicacao': 2022,
            'autores_nomes': ['OLIVEIRA, ANA PAULA DE']
        }
    ]
    
    # Criar as produções
    for producao_data in producoes_data:
        # Buscar autores
        autores_producao = []
        for nome_autor in producao_data['autores_nomes']:
            try:
                autor = Autor.objects.get(nome=nome_autor)
                autores_producao.append(autor)
            except Autor.DoesNotExist:
                print(f"⚠️ Autor não encontrado: {nome_autor}")
        
        # Criar produção
        producao, created = ProducaoBibliografica.objects.get_or_create(
            titulo=producao_data['titulo'],
            defaults={
                'link_producao': producao_data['link_producao'],
                'tipo': producao_data['tipo'],
                'local_publicacao': producao_data['local_publicacao'],
                'volume': producao_data['volume'],
                'numero': producao_data['numero'],
                'paginas': producao_data['paginas'],
                'ano_publicacao': producao_data['ano_publicacao'],
                'ativa': True
            }
        )
        
        if created:
            # Adicionar autores
            producao.autores.set(autores_producao)
            print(f"✅ Produção criada: {producao.titulo[:50]}...")
        else:
            print(f"ℹ️ Produção já existe: {producao.titulo[:50]}...")
    
    # Estatísticas finais
    total_autores = Autor.objects.count()
    total_producoes = ProducaoBibliografica.objects.filter(ativa=True).count()
    
    print(f"\n📊 Dados de teste criados com sucesso!")
    print(f"👥 Total de autores: {total_autores}")
    print(f"📚 Total de produções ativas: {total_producoes}")
    print(f"📅 Anos com produções: {list(ProducaoBibliografica.objects.filter(ativa=True).values_list('ano_publicacao', flat=True).distinct().order_by('-ano_publicacao'))}")
    
    # Distribuição por tipo
    from django.db.models import Count
    distribuicao_tipos = ProducaoBibliografica.objects.filter(ativa=True).values('tipo').annotate(count=Count('tipo')).order_by('-count')
    print(f"\n📈 Distribuição por tipo:")
    for item in distribuicao_tipos:
        tipo_display = dict(ProducaoBibliografica.TIPO_CHOICES)[item['tipo']]
        print(f"   {tipo_display}: {item['count']}")
    
    print(f"\n🎉 Script executado com sucesso!")
    print(f"💡 Acesse o admin do Django para gerenciar as produções bibliográficas.")
    print(f"🌐 Acesse a página de produções bibliográficas para ver o resultado.")


if __name__ == '__main__':
    criar_dados_teste()

