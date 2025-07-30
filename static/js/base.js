// JavaScript base para funcionalidades globais
document.addEventListener('DOMContentLoaded', function() {
    function createMobileMenu() {
        const mainNav = document.querySelector('.main-nav');
        const navList = document.querySelector('.main-nav-list');
        if (!mainNav || !navList) return;

        let navToggle = mainNav.querySelector('.nav-toggle');
        if (!navToggle) {
            navToggle = document.createElement('button');
            navToggle.className = 'nav-toggle';
            navToggle.setAttribute('aria-label', 'Toggle navigation menu');
            mainNav.insertBefore(navToggle, mainNav.firstChild);
        }

        navToggle.addEventListener('click', function() {
            const isActive = navList.classList.toggle('active');
            navToggle.classList.toggle('active');
            navToggle.setAttribute('aria-expanded', String(isActive));
        });
    }
    createMobileMenu();
});