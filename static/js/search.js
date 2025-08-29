document.addEventListener('DOMContentLoaded', () => {
    console.log('Search script loaded');
    
    // Usar os elementos da barra de pesquisa global existente
    const searchExpand = document.getElementById('searchExpand');
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');

    if (searchExpand && searchInput && searchBtn) {
        console.log('Elementos de pesquisa encontrados - funcionalidade já implementada no base.js');
        
        // Adicionar funcionalidade específica para páginas de pesquisa se necessário
        // A funcionalidade principal já está no base.js
        
        // Função para destacar resultados de pesquisa na página atual
        function highlightSearchResults() {
            const urlParams = new URLSearchParams(window.location.search);
            const query = urlParams.get('q');
            
            if (query && query.trim()) {
                console.log('Destacando resultados para:', query);
                highlightTextInPage(query.trim());
            }
        }
        
        // Função para destacar texto na página
        function highlightTextInPage(searchTerm) {
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                null,
                false
            );
            
            const textNodes = [];
            let node;
            
            while (node = walker.nextNode()) {
                if (node.parentElement.tagName !== 'SCRIPT' && 
                    node.parentElement.tagName !== 'STYLE' &&
                    node.textContent.toLowerCase().includes(searchTerm.toLowerCase())) {
                    textNodes.push(node);
                }
            }
            
            textNodes.forEach(textNode => {
                const parent = textNode.parentElement;
                const text = textNode.textContent;
                const regex = new RegExp(`(${searchTerm})`, 'gi');
                const highlightedText = text.replace(regex, '<mark style="background-color: #ffeb3b; padding: 2px 4px; border-radius: 2px;">$1</mark>');
                
                if (highlightedText !== text) {
                    const wrapper = document.createElement('span');
                    wrapper.innerHTML = highlightedText;
                    parent.replaceChild(wrapper, textNode);
                }
            });
        }
        
        // Executar destaque se houver parâmetro de busca na URL
        highlightSearchResults();
        
    } else {
        console.warn('Elementos de pesquisa não encontrados. Verifique se o base.html está carregado corretamente.');
    }
    
    // Funcionalidade adicional: busca em tempo real (opcional)
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    console.log('Busca em tempo real:', query);
                    // Aqui você pode implementar busca em tempo real se necessário
                }, 500);
            }
        });
    }
});