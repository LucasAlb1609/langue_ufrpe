/**
 * JavaScript para a página unificada de Produções Bibliográficas e Publicações PDF - LANGUE UFRPE
 */

document.addEventListener("DOMContentLoaded", function () {
    // Inicializar funcionalidades para Produções Bibliográficas
    initProducoesBibliograficas();

    // Inicializar funcionalidades para Publicações PDF
    initPublicacoesPDF();

    console.log("Página de Produções e Publicações carregada com sucesso");
});

/**
 * Funções para a seção de Produções Bibliográficas
 */
function initProducoesBibliograficas() {
    initExpandCollapse();
    initAnimationsProducoes();
    initAccessibilityProducoes();
    initSearchProducoes();
}

function initExpandCollapse() {
    const sections = document.querySelectorAll(".ano-producoes-section");
    if (sections.length > 0) {
        setTimeout(() => {
            const primeiraSecao = sections[0];
            const ano = primeiraSecao.id.replace("ano-", "");
            toggleAnoSection(parseInt(ano));
        }, 500);
    }
}

function toggleAnoSection(ano) {
    const section = document.getElementById(`ano-${ano}`);
    if (!section) return;

    const content = section.querySelector(".ano-producoes-content");
    const icon = section.querySelector(".expand-icon");

    if (section.classList.contains("retraida")) {
        section.classList.remove("retraida");
        section.classList.add("expandida");
        content.style.maxHeight = content.scrollHeight + "px";
        icon.style.transform = "rotate(180deg)";

        const producoes = content.querySelectorAll(".producao-item");
        producoes.forEach((producao, index) => {
            setTimeout(() => {
                producao.classList.add("animate-fade-in");
            }, index * 100);
        });

        announce(`Seção do ano ${ano} expandida`);
    } else {
        section.classList.remove("expandida");
        section.classList.add("retraida");
        content.style.maxHeight = "0";
        icon.style.transform = "rotate(0deg)";

        const producoes = content.querySelectorAll(".producao-item");
        producoes.forEach((producao) => {
            producao.classList.remove("animate-fade-in");
        });

        announce(`Seção do ano ${ano} retraída`);
    }
}

function initAnimationsProducoes() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px",
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("animate-fade-in");
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const sections = document.querySelectorAll(".ano-producoes-section");
    sections.forEach((section) => {
        observer.observe(section);
    });

    initParallaxEffect();
}

function initParallaxEffect() {
    const estatisticas = document.querySelector(".estatisticas-section");

    if (estatisticas && window.innerWidth > 768) {
        window.addEventListener(
            "scroll",
            throttle(() => {
                const rect = estatisticas.getBoundingClientRect();
                const scrolled = window.pageYOffset;
                const speed = 0.3;

                if (rect.top < window.innerHeight && rect.bottom > 0) {
                    const yPos = -(scrolled * speed);
                    estatisticas.style.transform = `translateY(${yPos}px)`;
                }
            }, 16)
        );
    }
}

function initAccessibilityProducoes() {
    initKeyboardNavigationProducoes();
    initScreenReaderAnnouncements();
}

function initKeyboardNavigationProducoes() {
    const headers = document.querySelectorAll(".ano-producoes-header");

    headers.forEach((header) => {
        header.setAttribute("tabindex", "0");
        header.setAttribute("role", "button");
        header.setAttribute("aria-expanded", "false");

        header.addEventListener("keydown", function (e) {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                this.click();

                const section = this.closest(".ano-producoes-section");
                const expanded = section.classList.contains("expandida");
                this.setAttribute("aria-expanded", expanded);
            }
        });
    });
}

function initScreenReaderAnnouncements() {
    const announcer = document.createElement("div");
    announcer.setAttribute("aria-live", "polite");
    announcer.setAttribute("aria-atomic", "true");
    announcer.className = "sr-only";
    announcer.id = "announcer";
    announcer.style.position = "absolute";
    announcer.style.left = "-10000px";
    announcer.style.width = "1px";
    announcer.style.height = "1px";
    announcer.style.overflow = "hidden";
    document.body.appendChild(announcer);
}

function announce(message) {
    const announcer = document.getElementById("announcer");
    if (announcer) {
        announcer.textContent = message;
        setTimeout(() => {
            announcer.textContent = "";
        }, 1000);
    }
}

function initSearchProducoes() {
    const searchInputGlobal = document.getElementById("searchInput");
    if (searchInputGlobal) {
        searchInputGlobal.addEventListener("input", function () {
            filtrarProducoes(this.value);
        });
    }
}

function filtrarProducoes(termo) {
    const sections = document.querySelectorAll(".ano-producoes-section");
    const searchTerm = termo.toLowerCase();
    let hasResults = false;

    sections.forEach((section) => {
        const producoes = section.querySelectorAll(".producao-item");
        let sectionHasResults = false;

        producoes.forEach((producao) => {
            const content = producao.textContent.toLowerCase();

            if (content.includes(searchTerm)) {
                producao.style.display = "block";
                highlightSearchTerm(producao, searchTerm);
                sectionHasResults = true;
                hasResults = true;
            } else {
                producao.style.display = "none";
            }
        });

        if (sectionHasResults) {
            section.style.display = "block";
            if (section.classList.contains("retraida")) {
                const ano = section.id.replace("ano-", "");
                toggleAnoSection(parseInt(ano));
            }
        } else {
            section.style.display = searchTerm ? "none" : "block";
        }
    });

    showSearchResultsProducoes(hasResults, termo);
}

function highlightSearchTerm(element, term) {
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );

    const textNodes = [];
    let node;

    while ((node = walker.nextNode())) {
        if (node.textContent.toLowerCase().includes(term)) {
            textNodes.push(node);
        }
    }

    textNodes.forEach((textNode) => {
        const parent = textNode.parentNode;
        const text = textNode.textContent;
        const regex = new RegExp(`(${term})`, "gi");
        const highlightedText = text.replace(regex, 
            `<mark class="search-highlight">$1</mark>`
        );

        if (highlightedText !== text) {
            const wrapper = document.createElement("span");
            wrapper.innerHTML = highlightedText;
            parent.replaceChild(wrapper, textNode);
        }
    });
}

function clearSearchResultsProducoes() {
    const sections = document.querySelectorAll(".ano-producoes-section");
    sections.forEach((section) => {
        section.style.display = "block";

        const producoes = section.querySelectorAll(".producao-item");
        producoes.forEach((producao) => {
            producao.style.display = "block";
        });

        const highlights = section.querySelectorAll(".search-highlight");
        highlights.forEach((highlight) => {
            const parent = highlight.parentNode;
            parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
            parent.normalize();
        });
    });

    hideSearchResultsProducoes();
}

function showSearchResultsProducoes(hasResults, query) {
    let resultsDiv = document.getElementById("search-results-producoes");

    if (!resultsDiv) {
        resultsDiv = document.createElement("div");
        resultsDiv.id = "search-results-producoes";
        resultsDiv.className = "search-results";
        document.querySelector(".secao-producoes-bibliograficas").prepend(resultsDiv);
    }

    if (hasResults) {
        resultsDiv.innerHTML = `
            <div class="search-results-content">
                <p>Resultados da busca por: "<strong>${query}</strong>"</p>
                <button onclick="clearSearchResultsProducoes()" class="clear-search-btn">Limpar busca</button>
            </div>
        `;
    } else {
        resultsDiv.innerHTML = `
            <div class="search-results-content no-results">
                <p>Nenhum resultado encontrado para: "<strong>${query}</strong>"</p>
                <button onclick="clearSearchResultsProducoes()" class="clear-search-btn">Limpar busca</button>
            </div>
        `;
    }

    resultsDiv.style.display = "block";
}

function hideSearchResultsProducoes() {
    const resultsDiv = document.getElementById("search-results-producoes");
    if (resultsDiv) {
        resultsDiv.style.display = "none";
    }
}

/**
 * Funções para a seção de Publicações PDF
 */
function initPublicacoesPDF() {
    const buscaInputPDF = document.getElementById("buscaPublicacoesPDF");
    const btnBuscarPDF = document.getElementById("btnBuscarPDF");
    const filtroCategoriaPDF = document.getElementById("filtroCategoriaPDF");
    const filtroAnoPDF = document.getElementById("filtroAnoPDF");
    const ordenacaoPDF = document.getElementById("ordenacaoPDF");
    const publicacaoCardsPDF = document.querySelectorAll(".secao-publicacoes-pdf .publicacao-card");

    let filtrosAtivosPDF = {
        busca: "",
        categoria: "",
        ano: "",
        ordenacao: "-ano_publicacao",
    };

    if (buscaInputPDF) {
        buscaInputPDF.addEventListener("input", debounce(handleBuscaPDF, 300));
        buscaInputPDF.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                handleBuscaPDF();
            }
        });
    }

    if (btnBuscarPDF) {
        btnBuscarPDF.addEventListener("click", handleBuscaPDF);
    }

    if (filtroCategoriaPDF) {
        filtroCategoriaPDF.addEventListener("change", handleFiltroCategoriaPDF);
    }

    if (filtroAnoPDF) {
        filtroAnoPDF.addEventListener("change", handleFiltroAnoPDF);
    }

    if (ordenacaoPDF) {
        ordenacaoPDF.addEventListener("change", handleOrdenacaoPDF);
    }

    animateCardsOnLoadPDF();
    setupLazyLoadingPDF();

    function handleBuscaPDF() {
        const termo = buscaInputPDF ? buscaInputPDF.value.toLowerCase().trim() : "";
        filtrosAtivosPDF.busca = termo;
        aplicarFiltrosPDF();
    }

    function handleFiltroCategoriaPDF() {
        filtrosAtivosPDF.categoria = filtroCategoriaPDF ? filtroCategoriaPDF.value : "";
        aplicarFiltrosPDF();
    }

    function handleFiltroAnoPDF() {
        filtrosAtivosPDF.ano = filtroAnoPDF ? filtroAnoPDF.value : "";
        aplicarFiltrosPDF();
    }

    function handleOrdenacaoPDF() {
        filtrosAtivosPDF.ordenacao = ordenacaoPDF ? ordenacaoPDF.value : "-ano_publicacao";
        aplicarFiltrosPDF();
    }

    function aplicarFiltrosPDF() {
        let publicacoesVisiveis = Array.from(publicacaoCardsPDF);

        if (filtrosAtivosPDF.busca) {
            publicacoesVisiveis = publicacoesVisiveis.filter((card) => {
                const titulo = card.dataset.titulo || "";
                const organizadores = card.dataset.organizadores || "";
                const categoria = card.dataset.categoria || "";

                const textoCompleto = `${titulo} ${organizadores} ${categoria}`.toLowerCase();
                return textoCompleto.includes(filtrosAtivosPDF.busca);
            });
        }

        if (filtrosAtivosPDF.categoria) {
            publicacoesVisiveis = publicacoesVisiveis.filter((card) => {
                return card.dataset.categoria === filtrosAtivosPDF.categoria;
            });
        }

        if (filtrosAtivosPDF.ano) {
            publicacoesVisiveis = publicacoesVisiveis.filter((card) => {
                return card.dataset.ano === filtrosAtivosPDF.ano;
            });
        }

        publicacoesVisiveis.sort((a, b) => {
            const campo = filtrosAtivosPDF.ordenacao.replace("-", "");
            const reverso = filtrosAtivosPDF.ordenacao.startsWith("-");

            let valorA, valorB;

            switch (campo) {
                case "ano_publicacao":
                    valorA = parseInt(a.dataset.ano) || 0;
                    valorB = parseInt(b.dataset.ano) || 0;
                    break;
                case "titulo":
                    valorA = a.dataset.titulo || "";
                    valorB = b.dataset.titulo || "";
                    break;
                case "downloads":
                    valorA = extrairDownloadsPDF(a);
                    valorB = extrairDownloadsPDF(b);
                    break;
                default:
                    return 0;
            }

            if (typeof valorA === "string") {
                const comparacao = valorA.localeCompare(valorB, "pt-BR");
                return reverso ? -comparacao : comparacao;
            } else {
                const comparacao = valorA - valorB;
                return reverso ? -comparacao : comparacao;
            }
        });

        publicacaoCardsPDF.forEach((card) => {
            if (publicacoesVisiveis.includes(card)) {
                mostrarCardPDF(card);
            } else {
                esconderCardPDF(card);
            }
        });

        publicacoesVisiveis.forEach((card, index) => {
            card.style.order = index;
        });

        mostrarMensagemSemResultadosPDF(publicacoesVisiveis.length === 0);
    }

    function extrairDownloadsPDF(card) {
        const metaItems = card.querySelectorAll(".meta-item");
        for (let item of metaItems) {
            const texto = item.textContent;
            if (texto.includes("download")) {
                const match = texto.match(/(\d+)/);
                return match ? parseInt(match[1]) : 0;
            }
        }
        return 0;
    }

    function mostrarCardPDF(card) {
        card.style.display = "flex";
        card.classList.remove("hidden");

        setTimeout(() => {
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, 10);
    }

    function esconderCardPDF(card) {
        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";

        setTimeout(() => {
            card.style.display = "none";
            card.classList.add("hidden");
        }, 300);
    }

    function mostrarMensagemSemResultadosPDF(mostrar) {
        let mensagem = document.querySelector(".secao-publicacoes-pdf .sem-resultados-filtro");

        if (mostrar && !mensagem) {
            mensagem = document.createElement("div");
            mensagem.className = "sem-resultados-filtro sem-publicacoes";
            mensagem.innerHTML = `
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" fill="none"/>
                    <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <h3>Nenhuma publicação encontrada</h3>
                <p>Não há publicações que correspondam aos filtros selecionados. Tente ajustar os critérios de busca.</p>
            `;
            document.querySelector("#publicacoesGridPDF").appendChild(mensagem);
        } else if (!mostrar && mensagem) {
            mensagem.remove();
        }
    }

    function animateCardsOnLoadPDF() {
        publicacaoCardsPDF.forEach((card, index) => {
            card.style.opacity = "0";
            card.style.transform = "translateY(30px)";

            setTimeout(() => {
                card.style.transition = "opacity 0.6s ease, transform 0.6s ease";
                card.style.opacity = "1";
                card.style.transform = "translateY(0)";
            }, index * 100);
        });
    }

    function setupLazyLoadingPDF() {
        if ("IntersectionObserver" in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute("data-src");
                        }
                        img.classList.remove("lazy");
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll(".secao-publicacoes-pdf img[data-src]").forEach((img) => {
                imageObserver.observe(img);
            });
        }
    }
}

/**
 * Funções utilitárias globais
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), limit);
        }
    };
}

function incrementarDownload(publicacaoId) {
    fetch(`/publicacoes/incrementar-download/${publicacaoId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCsrfToken(),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
    })
        .then((response) => {
            if (!response.ok) {
                console.warn("Erro ao incrementar contador de downloads");
            }
        })
        .catch((error) => {
            console.warn("Erro na requisição de incremento:", error);
        });
}

function getCsrfToken() {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split("=");
        if (name === "csrftoken") {
            return value;
        }
    }

    const csrfMeta = document.querySelector("meta[name=\"csrf-token\"]");
    return csrfMeta ? csrfMeta.getAttribute("content") : "";
}

function resetarFiltros() {
    const buscaInput = document.getElementById("buscaPublicacoesPDF");
    const filtroCategoria = document.getElementById("filtroCategoriaPDF");
    const filtroAno = document.getElementById("filtroAnoPDF");
    const ordenacao = document.getElementById("ordenacaoPDF");

    if (buscaInput) buscaInput.value = "";
    if (filtroCategoria) filtroCategoria.value = "";
    if (filtroAno) filtroAno.value = "";
    if (ordenacao) ordenacao.value = "-ano_publicacao";

    const event = new Event("input");
    if (buscaInput) buscaInput.dispatchEvent(event);
}

function exportarPublicacoes(formato = "csv") {
    console.log(`Exportando publicações em formato ${formato}...`);
}

function compartilharPublicacao(publicacaoId, titulo) {
    if (navigator.share) {
        navigator.share({
            title: titulo,
            text: `Confira esta publicação: ${titulo}`,
            url: window.location.href,
        }).catch((err) => console.log("Erro ao compartilhar:", err));
    } else {
        const url = `${window.location.origin}/publicacoes/#publicacao-${publicacaoId}`;
        navigator.clipboard.writeText(url).then(() => {
            mostrarNotificacao("Link copiado para a área de transferência!");
        }).catch((err) => {
            console.log("Erro ao copiar link:", err);
        });
    }
}

function mostrarNotificacao(mensagem, tipo = "success") {
    const notificacao = document.createElement("div");
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

    setTimeout(() => {
        notificacao.style.transform = "translateX(0)";
    }, 10);

    setTimeout(() => {
        notificacao.style.transform = "translateX(100%)";
        setTimeout(() => {
            document.body.removeChild(notificacao);
        }, 300);
    }, 3000);
}


