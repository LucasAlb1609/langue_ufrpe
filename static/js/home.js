// JavaScript para interatividade (ex: menu responsivo)

//Exemplo de toggle para menu responsivo (se necessário)
 document.addEventListener('DOMContentLoaded', function() {
     const navToggle = document.querySelector('.nav-toggle');
     const navLinks = document.querySelector('.nav-links');

     if (navToggle) {
         navToggle.addEventListener('click', function() {
             navLinks.classList.toggle('active');
         });
    }
 });

console.log("Script.js carregado com sucesso!");

