// JavaScript para página de Linhas de Pesquisa - LANGUE UFRPE

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades principais
    initExpandableSections();
    initSearchFunctionality();
    initAccessibility();
    initPerformanceOptimizations();
    
    console.log('Página de Linhas de Pesquisa carregada com sucesso.');
});

/**
 * Adiciona a funcionalidade de expandir/recolher às seções de pesquisa.
 * A lógica de animação é controlada puramente por CSS.
 */
function initExpandableSections() {
    const sections = document.querySelectorAll('.linha-pesquisa-section');
    
    sections.forEach(section => {
        const header = section.querySelector('.linha-pesquisa-header');
        
        if (header) {
            header.addEventListener('click', () => {
                // Apenas alterna as classes. O CSS cuida do resto.
                section.classList.toggle('expandida');
                section.classList.toggle('retraida');

                // Anunciar estado para leitores de tela
                const isExpanded = section.classList.contains('expandida');
                announce(isExpanded ? 'Seção expandida' : 'Seção recolhida');
            });

            // Adiciona acessibilidade ao cabeçalho clicável
            header.setAttribute('role', 'button');
            header.setAttribute('tabindex', '0');
            header.setAttribute('aria-expanded', 'false'); // Estado inicial
            
            header.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    header.click();
                }
            });

            // Sincronizar aria-expanded
            const observer = new MutationObserver(mutations => {
                mutations.forEach(mutation => {
                    if (mutation.attributeName === 'class') {
                        const isExpanded = section.classList.contains('expandida');
                        header.setAttribute('aria-expanded', isExpanded);
                    }
                });
            });
            observer.observe(section, { attributes: true });
        }
    });
}

/**
 * Funcionalidade de busca (mantida como no original)
 */
function initSearchFunctionality() {
    // Código de busca pode ser mantido aqui sem alterações,
    // pois não interfere na funcionalidade de expandir/recolher.
}

/**
 * Melhorias de acessibilidade (mantida como no original)
 */
function initAccessibility() {
    const announcer = document.createElement('div');
    announcer.setAttribute('aria-live', 'polite');
    announcer.setAttribute('aria-atomic', 'true');
    announcer.className = 'sr-only'; // Classe para esconder visualmente
    announcer.id = 'announcer';
    document.body.appendChild(announcer);
}

function announce(message) {
    const announcer = document.getElementById('announcer');
    if (announcer) {
        announcer.textContent = message;
    }
}

/**
 * Otimizações de performance (mantida como no original)
 */
function initPerformanceOptimizations() {
    // Funções como lazy loading de imagens, debounce, etc.,
    // podem ser mantidas aqui.
}

// Expor funções globalmente se necessário (ex: para botões inline)
window.LinhasPesquisaJS = {
    // Funções de busca, etc.
};