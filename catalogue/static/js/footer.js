/**
 * footer.js — Scripts du pied de page
 *
 * 1. Injecte l'année courante dans l'élément #year.
 * 2. Anime l'apparition du contenu footer au scroll (IntersectionObserver).
 */

document.addEventListener('DOMContentLoaded', function () {

    /* --- Mise à jour dynamique de l'année de copyright --- */
    const yearEl = document.getElementById('year');
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    /* --- Animation d'apparition au défilement --- */
    const footerContent = document.querySelector('.footer-inner');
    if (!footerContent) return;

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                footerContent.style.transition = 'all 1s cubic-bezier(0.2, 1, 0.3, 1)';
                footerContent.style.opacity = '1';
                footerContent.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.2 });

    observer.observe(footerContent);
});
