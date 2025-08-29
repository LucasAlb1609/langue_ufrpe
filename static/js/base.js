// JavaScript base para funcionalidades globais
document.addEventListener('DOMContentLoaded', function() {
    console.log("Base script loaded.");

    /**
     * INICIALIZAÇÃO DO MENU RESPONSIVO (HAMBÚRGUER)
     */
    function initMobileMenu() {
        const navToggle = document.getElementById('navToggle');
        const navList = document.getElementById('mainNavList');
        
        if (navToggle && navList) {
            // Marca como inicializado para evitar conflito com fallback
            navToggle.setAttribute('data-initialized', 'true');
            
            // Remove event listeners anteriores para evitar duplicação
            navToggle.removeEventListener('click', handleMenuToggle);
            navToggle.addEventListener('click', handleMenuToggle);

            function handleMenuToggle(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const isActive = navList.classList.toggle('active');
                navToggle.classList.toggle('active');
                navToggle.setAttribute('aria-expanded', isActive);
                
                console.log('Menu toggled:', isActive ? 'opened' : 'closed');
            }

            // Fecha o menu se o usuário clicar fora dele
            document.addEventListener('click', function(e) {
                if (navList.classList.contains('active') && 
                    !navToggle.contains(e.target) && 
                    !navList.contains(e.target)) {
                    
                    closeMenu();
                }
            });
            
            // Fecha o menu com tecla Escape
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && navList.classList.contains('active')) {
                    closeMenu();
                }
            });

            // Fecha ao clicar em um link
            const navLinks = navList.querySelectorAll('a');
            navLinks.forEach(link => {
                link.addEventListener('click', function() {
                    closeMenu();
                });
            });

            // Redefine em telas maiores
            window.addEventListener('resize', function() {
                if (window.innerWidth > 768 && navList.classList.contains('active')) {
                    closeMenu();
                }
            });

            function closeMenu() {
                navList.classList.remove('active');
                navToggle.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            }

            console.log('Menu hambúrguer inicializado com sucesso');
        } else {
            console.error('Elementos do menu não encontrados:', {
                navToggle: !!navToggle,
                navList: !!navList
            });
            
            // Tenta novamente após um pequeno delay
            setTimeout(initMobileMenu, 100);
        }
    }

    /**
     * INICIALIZAÇÃO DA BARRA DE PESQUISA EXPANSÍVEL
     */
    function initGlobalSearch() {
        const searchExpand = document.getElementById('searchExpand');
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');

        if (searchExpand && searchInput && searchBtn) {
            searchBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                
                if (!searchExpand.classList.contains('active')) {
                    searchExpand.classList.add('active');
                    searchInput.focus();
                    console.log('Search bar expanded');
                } else {
                    performSearch();
                }
            });

            searchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    performSearch();
                }
                if (e.key === 'Escape') {
                    searchExpand.classList.remove('active');
                    searchInput.value = '';
                }
            });
            
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

    function performSearch() {
        const query = document.getElementById('searchInput').value.trim();
        if (query) {
            console.log('Performing search for:', query);
            const encodedQuery = encodeURIComponent(query);
            try {
                window.location.href = `/search/?q=${encodedQuery}`;
            } catch (error) {
                console.error('Erro ao redirecionar para busca:', error);
                alert(`Busca por: "${query}"\n\nFuncionalidade de busca em desenvolvimento.`);
            }
        }
    }

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

    function initAccessibility() {
        const focusableElements = document.querySelectorAll(
            'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
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

    // Inicializações
    initMobileMenu();
    initGlobalSearch();
    highlightActiveNavLink();
    initAccessibility();
    
    console.log('Todas as funcionalidades base foram inicializadas.');
});
