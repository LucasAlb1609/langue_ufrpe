// JavaScript base para funcionalidades globais
document.addEventListener('DOMContentLoaded', function() {
    console.log("Base script loaded.");

    /**
     * INICIALIZAÇÃO DO MENU RESPONSIVO (HAMBÚRGUER)
     * Garante que o menu funcione em todas as páginas.
     */
    function initMobileMenu() {
        const mainNav = document.querySelector('.main-nav');
        const navList = document.querySelector('.main-nav-list');
        
        if (mainNav && navList) {
            // Garante que o botão só seja criado se não existir
            let navToggle = mainNav.querySelector('.nav-toggle');
            if (!navToggle) {
                navToggle = document.createElement('button');
                navToggle.className = 'nav-toggle';
                navToggle.setAttribute('aria-label', 'Alternar menu de navegação');
                navToggle.setAttribute('aria-expanded', 'false');
                // Adiciona o botão como o primeiro elemento dentro de .main-nav para melhor controle de layout
                mainNav.prepend(navToggle);
            }

            navToggle.addEventListener('click', function(e) {
                e.stopPropagation(); // Impede que o evento de clique se propague para o document
                const isActive = navList.classList.toggle('active');
                navToggle.classList.toggle('active');
                navToggle.setAttribute('aria-expanded', isActive);
            });

            // Fecha o menu se o usuário clicar fora dele
            document.addEventListener('click', function(e) {
                if (navList.classList.contains('active') && !mainNav.contains(e.target)) {
                    navList.classList.remove('active');
                    navToggle.classList.remove('active');
                    navToggle.setAttribute('aria-expanded', 'false');
                }
            });
            
            // Fecha o menu se a tecla 'Escape' for pressionada
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && navList.classList.contains('active')) {
                    navList.classList.remove('active');
                    navToggle.classList.remove('active');
                    navToggle.setAttribute('aria-expanded', 'false');
                }
            });

            // Garante que o menu seja redefinido em telas maiores
            window.addEventListener('resize', function() {
                if (window.innerWidth > 768 && navList.classList.contains('active')) {
                    navList.classList.remove('active');
                    navToggle.classList.remove('active');
                    navToggle.setAttribute('aria-expanded', 'false');
                }
            });
        }
    }

    /**
     * INICIALIZAÇÃO DA BARRA DE PESQUISA EXPANSÍVEL E FUNCIONAL
     * Garante que a busca funcione em todas as páginas.
     */
    function initGlobalSearch() {
        const searchExpand = document.getElementById('searchExpand');
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');

        if (searchExpand && searchInput && searchBtn) {
            searchBtn.addEventListener('click', function(e) {
                e.stopPropagation(); // Impede a propagação para o document
                
                // Se a barra não está ativa, ativa e foca no input
                if (!searchExpand.classList.contains('active')) {
                    searchExpand.classList.add('active');
                    searchInput.focus();
                } else {
                    // Se a barra já está ativa, executa a busca
                    performSearch();
                }
            });

            // Executa a busca ao pressionar Enter
            searchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    performSearch();
                }
                // Fecha a busca com a tecla Escape
                if (e.key === 'Escape') {
                    searchExpand.classList.remove('active');
                    searchInput.value = '';
                }
            });
            
            // Fecha a barra de busca ao clicar fora
            document.addEventListener('click', function(e) {
                if (searchExpand.classList.contains('active') && !searchExpand.contains(e.target)) {
                    searchExpand.classList.remove('active');
                    searchInput.value = '';
                }
            });
        }
    }

    /**
     * Redireciona para uma página de resultados de busca.
     * Esta página `/search/` precisa ser criada no seu `urls.py` e `views.py` do Django.
     */
    function performSearch() {
        const query = document.getElementById('searchInput').value.trim();
        if (query) {
            // Codifica a busca para ser segura na URL
            const encodedQuery = encodeURIComponent(query);
            // Redireciona para a página de busca
            window.location.href = `/search/?q=${encodedQuery}`;
        }
    }

    // Inicializa todas as funcionalidades globais
    initMobileMenu();
    initGlobalSearch();
});