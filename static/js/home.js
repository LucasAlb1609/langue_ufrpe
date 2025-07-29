// JavaScript otimizado para responsividade

document.addEventListener('DOMContentLoaded', function() {
    console.log("Script otimizado carregado com sucesso!");

    // Criar e inserir botão hambúrguer para mobile
    function createMobileMenu() {
        const mainNav = document.querySelector('.main-nav');
        const navList = document.querySelector('.main-nav-list');
        
        if (mainNav && navList) {
            // Criar botão hambúrguer se não existir
            let navToggle = document.querySelector('.nav-toggle');
            if (!navToggle) {
                navToggle = document.createElement('button');
                navToggle.className = 'nav-toggle';
                navToggle.setAttribute('aria-label', 'Toggle navigation menu');
                navToggle.setAttribute('aria-expanded', 'false');
                mainNav.appendChild(navToggle);
            }

            // Adicionar evento de clique ao botão hambúrguer
            navToggle.addEventListener('click', function() {
                const isActive = navList.classList.contains('active');
                
                navList.classList.toggle('active');
                navToggle.classList.toggle('active');
                
                // Atualizar aria-expanded para acessibilidade
                navToggle.setAttribute('aria-expanded', !isActive);
                
                // Fechar menu ao clicar em um link
                const navLinks = navList.querySelectorAll('a');
                navLinks.forEach(link => {
                    link.addEventListener('click', () => {
                        navList.classList.remove('active');
                        navToggle.classList.remove('active');
                        navToggle.setAttribute('aria-expanded', 'false');
                    });
                });
            });

            // Fechar menu ao clicar fora dele
            document.addEventListener('click', function(e) {
                if (!mainNav.contains(e.target) && navList.classList.contains('active')) {
                    navList.classList.remove('active');
                    navToggle.classList.remove('active');
                    navToggle.setAttribute('aria-expanded', 'false');
                }
            });

            // Fechar menu ao redimensionar para desktop
            window.addEventListener('resize', function() {
                if (window.innerWidth > 768) {
                    navList.classList.remove('active');
                    navToggle.classList.remove('active');
                    navToggle.setAttribute('aria-expanded', 'false');
                }
            });
        }
    }

    // Funcionalidade do campo de busca expansível
    function initSearchExpansion() {
        const searchBtn = document.getElementById('searchBtn');
        const searchExpand = document.getElementById('searchExpand');
        const searchInput = document.getElementById('searchInput');
        
        if (searchBtn && searchExpand && searchInput) {
            searchBtn.addEventListener('click', function(e) {
                e.preventDefault();
                searchExpand.classList.toggle('active');
                
                if (searchExpand.classList.contains('active')) {
                    searchInput.focus();
                    // Adicionar pequeno delay para garantir que o campo esteja visível
                    setTimeout(() => {
                        searchInput.focus();
                    }, 100);
                } else {
                    searchInput.value = '';
                    searchInput.blur();
                }
            });

            // Fechar o campo de busca ao clicar fora
            document.addEventListener('click', function(e) {
                if (!searchExpand.contains(e.target) && searchExpand.classList.contains('active')) {
                    searchExpand.classList.remove('active');
                    searchInput.value = '';
                    searchInput.blur();
                }
            });

            // Fechar com tecla Escape
            searchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    searchExpand.classList.remove('active');
                    searchInput.value = '';
                    searchInput.blur();
                }
            });

            // Submeter busca com Enter
            searchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const query = searchInput.value.trim();
                    if (query) {
                        console.log('Buscar por:', query);
                        // Aqui você pode implementar a lógica de busca
                        // Por exemplo: window.location.href = '/search?q=' + encodeURIComponent(query);
                    }
                }
            });
        }
    }

    // Melhorar experiência de toque em dispositivos móveis
    function improveTouchExperience() {
        // Adicionar classe para dispositivos touch
        if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
            document.body.classList.add('touch-device');
        }

        // Melhorar feedback visual para elementos tocáveis
        const touchableElements = document.querySelectorAll('a, button, .card');
        touchableElements.forEach(element => {
            element.addEventListener('touchstart', function() {
                this.classList.add('touch-active');
            });

            element.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.classList.remove('touch-active');
                }, 150);
            });
        });
    }

    // Lazy loading para imagens (melhoria de performance)
    function initLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback para navegadores sem suporte
            images.forEach(img => {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
            });
        }
    }

    // Smooth scroll para links internos
    function initSmoothScroll() {
        const internalLinks = document.querySelectorAll('a[href^="#"]');
        internalLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Detectar orientação do dispositivo
    function handleOrientationChange() {
        function updateOrientation() {
            const orientation = window.innerHeight > window.innerWidth ? 'portrait' : 'landscape';
            document.body.setAttribute('data-orientation', orientation);
        }

        updateOrientation();
        window.addEventListener('resize', updateOrientation);
        window.addEventListener('orientationchange', () => {
            setTimeout(updateOrientation, 100);
        });
    }

    // Inicializar todas as funcionalidades
    createMobileMenu();
    initSearchExpansion();
    improveTouchExperience();
    initLazyLoading();
    initSmoothScroll();
    handleOrientationChange();

    // Adicionar estilos CSS para feedback de toque via JavaScript
    const touchStyles = `
        <style>
            .touch-device .touch-active {
                opacity: 0.7;
                transform: scale(0.98);
                transition: opacity 0.1s, transform 0.1s;
            }
            
            .lazy {
                opacity: 0;
                transition: opacity 0.3s;
            }
            
            @media (max-width: 768px) {
                .nav-toggle {
                    display: block !important;
                }
                
                .main-nav-list {
                    display: flex !important;
                }
            }
        </style>
    `;
    
    document.head.insertAdjacentHTML('beforeend', touchStyles);
});

// Função utilitária para debounce (otimização de performance)
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Otimizar eventos de resize
const optimizedResize = debounce(() => {
    // Lógica para redimensionamento otimizada
    const event = new CustomEvent('optimizedResize');
    window.dispatchEvent(event);
}, 250);

window.addEventListener('resize', optimizedResize);

