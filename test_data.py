# Script para criar dados de teste para Linhas de Pesquisa
# Execute este script no shell do Django: python manage.py shell < test_data.py

from django.db import transaction
from linhas_pesquisa.models import LinhaPesquisa, Pesquisador, Estudante, ConfiguracaoPagina

def criar_dados_teste():
    """Cria dados de teste para o sistema de linhas de pesquisa"""
    
    with transaction.atomic():
        print("Criando dados de teste...")
        
        # Criar configuração da página
        configuracao, created = ConfiguracaoPagina.objects.get_or_create(
            defaults={
                'titulo_pagina': 'Linhas de Pesquisa',
                'descricao_pagina': 'Conheça as linhas de pesquisa desenvolvidas pelo LANGUE UFRPE, suas áreas de atuação e os pesquisadores envolvidos.'
            }
        )
        print(f"Configuração da página: {'criada' if created else 'já existia'}")
        
        # Criar pesquisadores
        pesquisadores_data = [
            {
                'nome': 'Natanael Duarte de Azevedo',
                'universidade': 'UFRPE',
                'link_lattes': 'http://lattes.cnpq.br/1234567890'
            },
            {
                'nome': 'Isabela Barbosa do Rego Barros',
                'universidade': 'UNICAP',
                'link_lattes': 'http://lattes.cnpq.br/2345678901'
            },
            {
                'nome': 'Leonardo Pinto Mendes',
                'universidade': 'UERJ',
                'link_lattes': 'http://lattes.cnpq.br/3456789012'
            },
            {
                'nome': 'Eduardo Barbuio',
                'universidade': 'UFRPE',
                'link_lattes': 'http://lattes.cnpq.br/4567890123'
            },
            {
                'nome': 'Iran Ferreira de Melo',
                'universidade': 'UFRPE',
                'link_lattes': 'http://lattes.cnpq.br/5678901234'
            },
            {
                'nome': 'Renata Barbosa Vicente',
                'universidade': 'UFRPE',
                'link_lattes': 'http://lattes.cnpq.br/6789012345'
            }
        ]
        
        pesquisadores = []
        for data in pesquisadores_data:
            pesquisador, created = Pesquisador.objects.get_or_create(
                nome=data['nome'],
                defaults=data
            )
            pesquisadores.append(pesquisador)
            print(f"Pesquisador {pesquisador.nome}: {'criado' if created else 'já existia'}")
        
        # Criar estudantes
        estudantes_data = [
            {
                'nome': 'Gleidson Rodrigues Teixeira da Silva',
                'nivel': 'PAVI',
                'universidade': 'UFRPE',
                'programa': 'Letras'
            },
            {
                'nome': 'Gleydson Araújo Gomes dos Santos',
                'nivel': 'PAVI',
                'universidade': 'UFRPE',
                'programa': 'Letras'
            },
            {
                'nome': 'Júlio Cesar da Silva',
                'nivel': 'PAVI',
                'universidade': 'UFRPE',
                'programa': 'Letras'
            },
            {
                'nome': 'Maria Isabela Berenguer de Menezes',
                'nivel': 'MESTRADO',
                'universidade': 'UFRPE',
                'programa': 'PROGEL',
                'link_lattes': 'http://lattes.cnpq.br/7890123456'
            },
            {
                'nome': 'Silmara Priscila Sabino Pereira da Silva',
                'nivel': 'MESTRADO',
                'universidade': 'UFRPE',
                'programa': 'PROGEL',
                'link_lattes': 'http://lattes.cnpq.br/8901234567'
            },
            {
                'nome': 'Ailton da Costa Silva Júnior',
                'nivel': 'DOUTORADO',
                'universidade': 'UFRPE',
                'programa': 'PGH',
                'link_lattes': 'http://lattes.cnpq.br/9012345678'
            },
            {
                'nome': 'Antônio Barros de Aguiar',
                'nivel': 'DOUTORADO',
                'universidade': 'UFRPE',
                'programa': 'PGH',
                'link_lattes': 'http://lattes.cnpq.br/0123456789'
            },
            {
                'nome': 'Camila Nadedja Teixeira Barbosa',
                'nivel': 'DOUTORADO',
                'universidade': 'UFRPE',
                'programa': 'PGH',
                'link_lattes': 'http://lattes.cnpq.br/1234567890'
            }
        ]
        
        estudantes = []
        for data in estudantes_data:
            estudante, created = Estudante.objects.get_or_create(
                nome=data['nome'],
                nivel=data['nivel'],
                universidade=data['universidade'],
                defaults=data
            )
            estudantes.append(estudante)
            print(f"Estudante {estudante.nome}: {'criado' if created else 'já existia'}")
        
        # Criar linhas de pesquisa
        linha1_data = {
            'titulo': 'História da Literatura: trajetórias literárias em impressos dos séculos XIX e XX',
            'objetivo': 'A literatura presente nos periódicos caracterizou a realidade da literatura nacional no grande século XIX e permaneceu até século XX, fazendo com que esse suporte veiculasse grande parte das obras literárias e dos manifestos artístico-políticos no cenário brasileiro. O objetivo de nossa pesquisa é compreender os discursos que circulavam nos jornais catalogados e a sua relação com a História da Literatura.',
            'palavras_chave': 'História da literatura; História da Leitura; Literatura dos Oitocentos; Crítica social; Sátira e paródia',
            'setores_aplicacao': 'Edição integrada à impressão de livros, jornais, revistas e outras publicações.',
            'ordem': 1
        }
        
        linha2_data = {
            'titulo': 'Linguagem, Gênero e Relações de poder: a ascensão das minorias',
            'objetivo': 'Trabalhar os conceitos de cultura e de linguagem. Analisar os discursos hegemônicos que organizam e engendram o comportamento do sujeito na sociedade ocidental. Identificar como a cultura patriarcal exclui das regras civis a inserção dos discursos dos grupos minoritários na sociedade burguesa, bem como averiguar como as artes, designadas eruditas, forjaram o código de comportamento de gênero social e foram cooptadas para o engendramento das práticas sociais da burguesia.',
            'palavras_chave': 'Linguagem; Relações de gênero; Relações de Poder; Minorias; Cultura patriarcal',
            'setores_aplicacao': 'Pesquisa e desenvolvimento experimental em ciências sociais e humanas; Educação superior.',
            'ordem': 2
        }
        
        # Criar primeira linha de pesquisa
        linha1, created = LinhaPesquisa.objects.get_or_create(
            titulo=linha1_data['titulo'],
            defaults=linha1_data
        )
        print(f"Linha de pesquisa 1: {'criada' if created else 'já existia'}")
        
        # Adicionar pesquisadores à linha 1
        linha1.pesquisadores.add(pesquisadores[0])  # Natanael (coordenador)
        linha1.pesquisadores.add(pesquisadores[1])  # Isabela
        linha1.pesquisadores.add(pesquisadores[2])  # Leonardo
        
        # Adicionar estudantes à linha 1
        linha1.estudantes.add(estudantes[0])  # Gleidson (PAVI)
        linha1.estudantes.add(estudantes[1])  # Gleydson (PAVI)
        linha1.estudantes.add(estudantes[2])  # Júlio (PAVI)
        linha1.estudantes.add(estudantes[3])  # Maria Isabela (Mestrado)
        linha1.estudantes.add(estudantes[4])  # Silmara (Mestrado)
        
        # Criar segunda linha de pesquisa
        linha2, created = LinhaPesquisa.objects.get_or_create(
            titulo=linha2_data['titulo'],
            defaults=linha2_data
        )
        print(f"Linha de pesquisa 2: {'criada' if created else 'já existia'}")
        
        # Adicionar pesquisadores à linha 2
        linha2.pesquisadores.add(pesquisadores[0])  # Natanael (coordenador)
        linha2.pesquisadores.add(pesquisadores[3])  # Eduardo
        linha2.pesquisadores.add(pesquisadores[4])  # Iran
        linha2.pesquisadores.add(pesquisadores[5])  # Renata
        
        # Adicionar estudantes à linha 2
        linha2.estudantes.add(estudantes[5])  # Ailton (Doutorado)
        linha2.estudantes.add(estudantes[6])  # Antônio (Doutorado)
        linha2.estudantes.add(estudantes[7])  # Camila (Doutorado)
        
        print("\nDados de teste criados com sucesso!")
        print(f"Total de pesquisadores: {Pesquisador.objects.count()}")
        print(f"Total de estudantes: {Estudante.objects.count()}")
        print(f"Total de linhas de pesquisa: {LinhaPesquisa.objects.count()}")

if __name__ == "__main__":
    criar_dados_teste()

