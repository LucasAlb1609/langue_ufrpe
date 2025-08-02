// JavaScript para página de Produções Bibliográficas - LANGUE UFRPE

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades
    initSearchFunctionality();
    initAnimations();
    initAccessibility();
    initPerformanceOptimizations();
    initExpandCollapse();
    
    console.log('Página de Produções Bibliográficas carregada com sucesso');
});

/**
 * Funcionalidade de busca
 */
function initSearchFunctionality() {
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    const searchExpand = document.getElementById('searchExpand');
    
    if (!searchBtn || !searchInput || !searchExpand) return;
    
    // Toggle da barra de busca
    searchBtn.addEventListener('click', function(e) {
        e.preventDefault();
        toggleSearch();
    });
    
    // Busca ao pressionar Enter
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            performSearch(this.value);
        }
    });
    
    // Busca em tempo real
    searchInput.addEventListener('input', function(e) {
        performSearch(this.value);
    });
    
    // Fechar busca ao clicar fora
    document.addEventListener('click', function(e) {
        if (!searchExpand.contains(e.target) && searchExpand.classList.contains('active')) {
            closeSearch();
        }
    });
    
    // Fechar busca com ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && searchExpand.classList.contains('active')) {
            closeSearch();
        }
    });
}

function toggleSearch() {
    const searchExpand = document.getElementById('searchExpand');
    const searchInput = document.getElementById('searchInput');
    
    if (searchExpand.classList.contains('active')) {
        closeSearch();
    } else {
        openSearch();
    }
}

function openSearch() {
    const searchExpand = document.getElementById('searchExpand');
    const searchInput = document.getElementById('searchInput');
    
    searchExpand.classList.add('active');
    setTimeout(() => {
        searchInput.focus();
    }, 300);
}

function closeSearch() {
    const searchExpand = document.getElementById('searchExpand');
    const searchInput = document.getElementById('searchInput');
    
    searchExpand.classList.remove('active');
    searchInput.value = '';
    clearSearchResults();
}

function performSearch(query) {
    if (!query.trim()) {
        clearSearchResults();
        return;
    }
    
    const sections = document.querySelectorAll('.ano-producoes-section');
    const searchTerm = query.toLowerCase();
    let hasResults = false;
    
    sections.forEach(section => {
        const producoes = section.querySelectorAll('.producao-item');
        let sectionHasResults = false;
        
        producoes.forEach(producao => {
            const content = producao.textContent.toLowerCase();
            
            if (content.includes(searchTerm)) {
                producao.style.display = 'block';
                highlightSearchTerm(producao, searchTerm);
                sectionHasResults = true;
                hasResults = true;
            } else {
                producao.style.display = 'none';
            }
        });
        
        // Mostrar/ocultar seção baseado nos resultados
        if (sectionHasResults) {
            section.style.display = 'block';
            // Expandir automaticamente se houver resultados
            if (section.classList.contains('retraida')) {
                const ano = section.id.replace('ano-', '');
                toggleAnoSection(parseInt(ano));
            }
        } else {
            section.style.display = 'none';
        }
    });
    
    showSearchResults(hasResults, query);
}

function highlightSearchTerm(element, term) {
    // Implementação básica de highlight
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    const textNodes = [];
    let node;
    
    while (node = walker.nextNode()) {
        if (node.textContent.toLowerCase().includes(term)) {
            textNodes.push(node);
        }
    }
    
    textNodes.forEach(textNode => {
        const parent = textNode.parentNode;
        const text = textNode.textContent;
        const regex = new RegExp(`(${term})`, 'gi');
        const highlightedText = text.replace(regex, '<mark class="search-highlight">$1</mark>');
        
        if (highlightedText !== text) {
            const wrapper = document.createElement('span');
            wrapper.innerHTML = highlightedText;
            parent.replaceChild(wrapper, textNode);
        }
    });
}

function clearSearchResults() {
    const sections = document.querySelectorAll('.ano-producoes-section');
    sections.forEach(section => {
        section.style.display = 'block';
        
        const producoes = section.querySelectorAll('.producao-item');
        producoes.forEach(producao => {
            producao.style.display = 'block';
        });
        
        // Remover highlights
        const highlights = section.querySelectorAll('.search-highlight');
        highlights.forEach(highlight => {
            const parent = highlight.parentNode;
            parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
            parent.normalize();
        });
    });
    
    hideSearchResults();
}

function showSearchResults(hasResults, query) {
    let resultsDiv = document.getElementById('search-results');
    
    if (!resultsDiv) {
        resultsDiv = document.createElement('div');
        resultsDiv.id = 'search-results';
        resultsDiv.className = 'search-results';
        document.querySelector('.producoes-bibliograficas-main').prepend(resultsDiv);
    }
    
    if (hasResults) {
        resultsDiv.innerHTML = `
            <div class="search-results-content">
                <p>Resultados da busca por: "<strong>${query}</strong>"</p>
                <button onclick="clearSearchResults()" class="clear-search-btn">Limpar busca</button>
            </div>
        `;
    } else {
        resultsDiv.innerHTML = `
            <div class="search-results-content no-results">
                <p>Nenhum resultado encontrado para: "<strong>${query}</strong>"</p>
                <button onclick="clearSearchResults()" class="clear-search-btn">Limpar busca</button>
            </div>
        `;
    }
    
    resultsDiv.style.display = 'block';
}

function hideSearchResults() {
    const resultsDiv = document.getElementById('search-results');
    if (resultsDiv) {
        resultsDiv.style.display = 'none';
    }
}

/**
 * Funcionalidade de expandir/recolher seções por ano
 */
function initExpandCollapse() {
    // Expandir automaticamente o ano mais recente
    const sections = document.querySelectorAll('.ano-producoes-section');
    if (sections.length > 0) {
        setTimeout(() => {
            const primeiraSecao = sections[0];
            const ano = primeiraSecao.id.replace('ano-', '');
            toggleAnoSection(parseInt(ano));
        }, 500);
    }
}

function toggleAnoSection(ano) {
    const section = document.getElementById(`ano-${ano}`);
    if (!section) return;
    
    const content = section.querySelector('.ano-producoes-content');
    const icon = section.querySelector('.expand-icon');
    
    if (section.classList.contains('retraida')) {
        // Expandir
        section.classList.remove('retraida');
        section.classList.add('expandida');
        content.style.maxHeight = content.scrollHeight + 'px';
        icon.style.transform = 'rotate(180deg)';
        
        // Animar as produções
        const producoes = content.querySelectorAll('.producao-item');
        producoes.forEach((producao, index) => {
            setTimeout(() => {
                producao.classList.add('animate-fade-in');
            }, index * 100);
        });
        
        // Anunciar para leitores de tela
        announce(`Seção do ano ${ano} expandida`);
    } else {
        // Retrair
        section.classList.remove('expandida');
        section.classList.add('retraida');
        content.style.maxHeight = '0';
        icon.style.transform = 'rotate(0deg)';
        
        // Remover animações
        const producoes = content.querySelectorAll('.producao-item');
        producoes.forEach(producao => {
            producao.classList.remove('animate-fade-in');
        });
        
        // Anunciar para leitores de tela
        announce(`Seção do ano ${ano} retraída`);
    }
}

/**
 * Animações e efeitos visuais
 */
function initAnimations() {
    // Intersection Observer para animações de entrada
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observar seções de ano
    const sections = document.querySelectorAll('.ano-producoes-section');
    sections.forEach(section => {
        observer.observe(section);
    });
    
    // Efeito parallax suave para estatísticas
    initParallaxEffect();
}

function initParallaxEffect() {
    const estatisticas = document.querySelector('.estatisticas-section');
    
    if (estatisticas && window.innerWidth > 768) { // Apenas em desktop
        window.addEventListener('scroll', throttle(() => {
            const rect = estatisticas.getBoundingClientRect();
            const scrolled = window.pageYOffset;
            const speed = 0.3;
            
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                const yPos = -(scrolled * speed);
                estatisticas.style.transform = `translateY(${yPos}px)`;
            }
        }, 16));
    }
}

/**
 * Melhorias de acessibilidade
 */
function initAccessibility() {
    // Navegação por teclado
    initKeyboardNavigation();
    
    // Anúncios para leitores de tela
    initScreenReaderAnnouncements();
    

}

function initKeyboardNavigation() {
    const headers = document.querySelectorAll('.ano-producoes-header');
    
    headers.forEach(header => {
        // Tornar clicável por teclado
        header.setAttribute('tabindex', '0');
        header.setAttribute('role', 'button');
        header.setAttribute('aria-expanded', 'false');
        
        header.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
                
                // Atualizar aria-expanded
                const section = this.closest('.ano-producoes-section');
                const expanded = section.classList.contains('expandida');
                this.setAttribute('aria-expanded', expanded);
            }
        });
    });
}

function initScreenReaderAnnouncements() {
    // Criar região para anúncios
    const announcer = document.createElement('div');
    announcer.setAttribute('aria-live', 'polite');
    announcer.setAttribute('aria-atomic', 'true');
    announcer.className = 'sr-only';
    announcer.id = 'announcer';
    announcer.style.position = 'absolute';
    announcer.style.left = '-10000px';
    announcer.style.width = '1px';
    announcer.style.height = '1px';
    announcer.style.overflow = 'hidden';
    document.body.appendChild(announcer);
}

function announce(message) {
    const announcer = document.getElementById('announcer');
    if (announcer) {
        announcer.textContent = message;
        setTimeout(() => {
            announcer.textContent = '';
        }, 1000);
    }
}



