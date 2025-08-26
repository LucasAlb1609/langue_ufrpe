// JavaScript ESPECÍFICO para a página Home

document.addEventListener('DOMContentLoaded', function () {
    /**
     * Funcionalidade para expandir/recolher a seção "Sobre o LANGUE"
     */
    function initAboutSectionToggle() {
        const menuLangueLink = document.querySelector('a[href="#langue"]');
        const aboutSection = document.querySelector('.about-langue-section');

        if (menuLangueLink && aboutSection) {
            menuLangueLink.addEventListener('click', function (e) {
                e.preventDefault();

                const isExpanded = aboutSection.classList.contains('show');

                if (!isExpanded) {
                    aboutSection.classList.add('show');
                    aboutSection.style.maxHeight = aboutSection.scrollHeight + 'px';
                    aboutSection.style.opacity = '1';
                    aboutSection.style.transition = 'max-height 0.7s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.5s ease';
                    // Rola suavemente até a seção revelada
                    setTimeout(() => {
                        aboutSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 100); // Aguarda início da animação
                } else {
                    aboutSection.classList.remove('show');
                    aboutSection.style.maxHeight = '0';
                    aboutSection.style.opacity = '0';
                    aboutSection.style.transition = 'max-height 0.5s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.4s ease';
                }
            });
        }
    }

    /**
     * Outras funcionalidades específicas da home page podem ser adicionadas aqui.
     */
    function initHomePageFeatures() {
        // Lazy loading para imagens (melhoria de performance)
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
            images.forEach(img => {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
            });
        }

        // Smooth scroll para links internos da home
        const internalLinks = document.querySelectorAll('a[href^="#"]');
        internalLinks.forEach(link => {
            // Ignora o link do toggle da seção about
            if (link.getAttribute('href') !== '#langue') {
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
            }
        });
    }

    // Inicializa todas as funcionalidades da home page
    initAboutSectionToggle();
    initHomePageFeatures();

    console.log("Home script loaded.");
});