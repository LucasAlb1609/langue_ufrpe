// JavaScript base para funcionalidades globais
document.addEventListener('DOMContentLoaded', function() {
    console.log("Base script loaded.");

    /**
     * INICIALIZAÇÃO DO MENU RESPONSIVO (HAMBÚRGUER)
     * Versão corrigida que funciona com o botão já presente no HTML
     */
    function initMobileMenu() {
        const navToggle = document.getElementById('navToggle');
        const navList = document.getElementById('mainNavList');
        
        if (navToggle && navList) {
            navToggle.addEventListener('click', function(e) {
                e.stopPropagation(); // Impede que o evento se propague
                
                const isActive = navList.classList.toggle('active');
                navToggle.classList.toggle('active');
                navToggle.setAttribute('aria-expanded', isActive);
                
                // Log para debug
                console.log('Menu toggled:', isActive ? 'opened' : 'closed');
            });

            // Fecha o menu se o usuário clicar fora dele
            document.addEventListener('click', function(e) {
                if (navList.classList.contains('active') && 
                    !navToggle.contains(e.target) && 
                    !navList.contains(e.target)) {
                    
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

            // Fecha o menu ao clicar em um link (navegação)
            const navLinks = navList.querySelectorAll('a');
            navLinks.forEach(link => {
                link.addEventListener('click', function() {
                    navList.classList.remove('active');
                    navToggle.classList.remove('active');
                    navToggle.setAttribute('aria-expanded', 'false');
                });
            });

            // Garante que o menu seja redefinido em telas maiores
            window.addEventListener('resize', function() {
                if (window.innerWidth > 1024 && navList.classList.contains('active')) {
                    navList.classList.remove('active');
                    navToggle.classList.remove('active');
                    navToggle.setAttribute('aria-expanded', 'false');
                }
            });
        } else {
            console.error('Elementos do menu não encontrados:', {
                navToggle: !!navToggle,
                navList: !!navList
            });
        }
    }

    /**
     * INICIALIZAÇÃO DA BARRA DE PESQUISA EXPANSÍVEL E FUNCIONAL
     * Versão corrigida que funciona em todas as páginas
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
                    console.log('Search bar expanded');
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
        } else {
            console.error('Elementos da busca não encontrados:', {
                searchExpand: !!searchExpand,
                searchInput: !!searchInput,
                searchBtn: !!searchBtn
            });
        }
    }

    /**
     * Executa a busca - versão melhorada com fallback
     */
    function performSearch() {
        const query = document.getElementById('searchInput').value.trim();
        if (query) {
            console.log('Performing search for:', query);
            
            // Codifica a busca para ser segura na URL
            const encodedQuery = encodeURIComponent(query);
            
            // Tenta redirecionar para a página de busca
            // Se a rota não existir, mostra um alerta
            try {
                window.location.href = `/search/?q=${encodedQuery}`;
            } catch (error) {
                console.error('Erro ao redirecionar para busca:', error);
                alert(`Busca por: "${query}"\n\nFuncionalidade de busca em desenvolvimento.`);
            }
        }
    }

    /**
     * Função para destacar o link ativo no menu
     */
    function highlightActiveNavLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.main-nav-list a');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }

    /**
     * Função para melhorar a acessibilidade
     */
    function initAccessibility() {
        // Adiciona suporte a navegação por teclado
        const focusableElements = document.querySelectorAll(
            'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        // Melhora o contraste de foco
        focusableElements.forEach(element => {
            element.addEventListener('focus', function() {
                this.style.outline = '2px solid #961120';
                this.style.outlineOffset = '2px';
            });
            
            element.addEventListener('blur', function() {
                this.style.outline = '';
                this.style.outlineOffset = '';
            });
        });
    }

    // Inicializa todas as funcionalidades globais
    initMobileMenu();
    initGlobalSearch();
    highlightActiveNavLink();
    initAccessibility();
    
    console.log('Todas as funcionalidades base foram inicializadas.');
});

