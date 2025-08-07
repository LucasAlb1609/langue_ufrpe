/**
 * JavaScript para a página de Publicações PDF - LANGUE UFRPE
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const buscaInput = document.getElementById('buscaPublicacoes');
    const btnBuscar = document.getElementById('btnBuscar');
    const filtroCategoria = document.getElementById('filtroCategoria');
    const filtroAno = document.getElementById('filtroAno');
    const ordenacao = document.getElementById('ordenacao');
    const publicacoesGrid = document.getElementById('publicacoesGrid');
    const publicacaoCards = document.querySelectorAll('.publicacao-card');

    // Estado dos filtros
    let filtrosAtivos = {
        busca: '',
        categoria: '',
        ano: '',
        ordenacao: '-ano_publicacao'
    };

    // Inicialização
    init();

    function init() {
        // Event listeners
        if (buscaInput) {
            buscaInput.addEventListener('input', debounce(handleBusca, 300));
            buscaInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    handleBusca();
                }
            });
        }

        if (btnBuscar) {
            btnBuscar.addEventListener('click', handleBusca);
        }

        if (filtroCategoria) {
            filtroCategoria.addEventListener('change', handleFiltroCategoria);
        }

        if (filtroAno) {
            filtroAno.addEventListener('change', handleFiltroAno);
        }

        if (ordenacao) {
            ordenacao.addEventListener('change', handleOrdenacao);
        }

        // Animações de entrada
        animateCardsOnLoad();

        // Lazy loading para imagens
        setupLazyLoading();
    }

    /**
     * Manipula a busca por texto
     */
    function handleBusca() {
        const termo = buscaInput ? buscaInput.value.toLowerCase().trim() : '';
        filtrosAtivos.busca = termo;
        aplicarFiltros();
    }

    /**
     * Manipula o filtro por categoria
     */
    function handleFiltroCategoria() {
        filtrosAtivos.categoria = filtroCategoria ? filtroCategoria.value : '';
        aplicarFiltros();
    }

    /**
     * Manipula o filtro por ano
     */
    function handleFiltroAno() {
        filtrosAtivos.ano = filtroAno ? filtroAno.value : '';
        aplicarFiltros();
    }

    /**
     * Manipula a ordenação
     */
    function handleOrdenacao() {
        filtrosAtivos.ordenacao = ordenacao ? ordenacao.value : '-ano_publicacao';
        aplicarFiltros();
    }

    /**
     * Aplica todos os filtros ativos
     */
    function aplicarFiltros() {
        let publicacoesVisiveis = Array.from(publicacaoCards);

        // Filtro por busca
        if (filtrosAtivos.busca) {
            publicacoesVisiveis = publicacoesVisiveis.filter(card => {
                const titulo = card.dataset.titulo || '';
                const organizadores = card.dataset.organizadores || '';
                const categoria = card.dataset.categoria || '';
                
                const textoCompleto = `${titulo} ${organizadores} ${categoria}`.toLowerCase();
                return textoCompleto.includes(filtrosAtivos.busca);
            });
        }

        // Filtro por categoria
        if (filtrosAtivos.categoria) {
            publicacoesVisiveis = publicacoesVisiveis.filter(card => {
                return card.dataset.categoria === filtrosAtivos.categoria;
            });
        }

        // Filtro por ano
        if (filtrosAtivos.ano) {
            publicacoesVisiveis = publicacoesVisiveis.filter(card => {
                return card.dataset.ano === filtrosAtivos.ano;
            });
        }

        // Ordenação
        publicacoesVisiveis.sort((a, b) => {
            const campo = filtrosAtivos.ordenacao.replace('-', '');
            const reverso = filtrosAtivos.ordenacao.startsWith('-');

            let valorA, valorB;

            switch (campo) {
                case 'ano_publicacao':
                    valorA = parseInt(a.dataset.ano) || 0;
                    valorB = parseInt(b.dataset.ano) || 0;
                    break;
                case 'titulo':
                    valorA = a.dataset.titulo || '';
                    valorB = b.dataset.titulo || '';
                    break;
                case 'downloads':
                    // Extrair número de downloads do texto
                    const downloadsA = extrairDownloads(a);
                    const downloadsB = extrairDownloads(b);
                    valorA = downloadsA;
                    valorB = downloadsB;
                    break;
                default:
                    return 0;
            }

            if (typeof valorA === 'string') {
                const comparacao = valorA.localeCompare(valorB, 'pt-BR');
                return reverso ? -comparacao : comparacao;
            } else {
                const comparacao = valorA - valorB;
                return reverso ? -comparacao : comparacao;
            }
        });

        // Aplicar visibilidade
        publicacaoCards.forEach(card => {
            if (publicacoesVisiveis.includes(card)) {
                mostrarCard(card);
            } else {
                esconderCard(card);
            }
        });

        // Reordenar no DOM
        publicacoesVisiveis.forEach((card, index) => {
            card.style.order = index;
        });

        // Mostrar mensagem se não há resultados
        mostrarMensagemSemResultados(publicacoesVisiveis.length === 0);
    }

    /**
     * Extrai o número de downloads de um card
     */
    function extrairDownloads(card) {
        const metaItems = card.querySelectorAll('.meta-item');
        for (let item of metaItems) {
            const texto = item.textContent;
            if (texto.includes('download')) {
                const match = texto.match(/(\d+)/);
                return match ? parseInt(match[1]) : 0;
            }
        }
        return 0;
    }

    /**
     * Mostra um card com animação
     */
    function mostrarCard(card) {
        card.style.display = 'flex';
        card.classList.remove('hidden');
        
        // Pequeno delay para permitir a transição
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 10);
    }

    /**
     * Esconde um card com animação
     */
    function esconderCard(card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.display = 'none';
            card.classList.add('hidden');
        }, 300);
    }

    /**
     * Mostra/esconde mensagem quando não há resultados
     */
    function mostrarMensagemSemResultados(mostrar) {
        let mensagem = document.querySelector('.sem-resultados-filtro');
        
        if (mostrar && !mensagem) {
            mensagem = document.createElement('div');
            mensagem.className = 'sem-resultados-filtro sem-publicacoes';
            mensagem.innerHTML = `
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" fill="none"/>
                    <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <h3>Nenhuma publicação encontrada</h3>
                <p>Não há publicações que correspondam aos filtros selecionados. Tente ajustar os critérios de busca.</p>
            `;
            publicacoesGrid.appendChild(mensagem);
        } else if (!mostrar && mensagem) {
            mensagem.remove();
        }
    }

    /**
     * Anima os cards na carga inicial
     */
    function animateCardsOnLoad() {
        publicacaoCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    /**
     * Configura lazy loading para imagens
     */
    function setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    /**
     * Função debounce para otimizar performance
     */
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
});

/**
 * Função global para incrementar downloads
 * Chamada quando um PDF é clicado
 */
function incrementarDownload(publicacaoId) {
    // Enviar requisição AJAX para incrementar contador
    fetch(`/publicacoes/incrementar-download/${publicacaoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (!response.ok) {
            console.warn('Erro ao incrementar contador de downloads');
        }
    })
    .catch(error => {
        console.warn('Erro na requisição de incremento:', error);
    });
}

/**
 * Obtém o token CSRF do Django
 */
function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    
    // Fallback: buscar no meta tag
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    return csrfMeta ? csrfMeta.getAttribute('content') : '';
}

/**
 * Função para resetar todos os filtros
 */
function resetarFiltros() {
    const buscaInput = document.getElementById('buscaPublicacoes');
    const filtroCategoria = document.getElementById('filtroCategoria');
    const filtroAno = document.getElementById('filtroAno');
    const ordenacao = document.getElementById('ordenacao');

    if (buscaInput) buscaInput.value = '';
    if (filtroCategoria) filtroCategoria.value = '';
    if (filtroAno) filtroAno.value = '';
    if (ordenacao) ordenacao.value = '-ano_publicacao';

    // Reaplica os filtros (que agora estão limpos)
    const event = new Event('input');
    if (buscaInput) buscaInput.dispatchEvent(event);
}

/**
 * Função para exportar lista de publicações (futura implementação)
 */
function exportarPublicacoes(formato = 'csv') {
    console.log(`Exportando publicações em formato ${formato}...`);
    // Implementação futura para exportar dados
}

/**
 * Função para compartilhar publicação
 */
function compartilharPublicacao(publicacaoId, titulo) {
    if (navigator.share) {
        navigator.share({
            title: titulo,
            text: `Confira esta publicação: ${titulo}`,
            url: window.location.href
        }).catch(err => console.log('Erro ao compartilhar:', err));
    } else {
        // Fallback: copiar URL para clipboard
        const url = `${window.location.origin}/publicacoes/#publicacao-${publicacaoId}`;
        navigator.clipboard.writeText(url).then(() => {
            // Mostrar feedback visual
            mostrarNotificacao('Link copiado para a área de transferência!');
        }).catch(err => {
            console.log('Erro ao copiar link:', err);
        });
    }
}

/**
 * Mostra notificação temporária
 */
function mostrarNotificacao(mensagem, tipo = 'success') {
    const notificacao = document.createElement('div');
    notificacao.className = `notificacao notificacao-${tipo}`;
    notificacao.textContent = mensagem;
    notificacao.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;

    document.body.appendChild(notificacao);

    // Anima entrada
    setTimeout(() => {
        notificacao.style.transform = 'translateX(0)';
    }, 10);

    // Remove após 3 segundos
    setTimeout(() => {
        notificacao.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notificacao);
        }, 300);
    }, 3000);
}

