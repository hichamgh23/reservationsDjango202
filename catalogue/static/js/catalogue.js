/**
 * catalogue.js — Comportements des pages de liste (spectacles, artistes, localités)
 *
 * Applique un délai de stagger (décalage progressif) aux éléments animés
 * via l'attribut data-animate-index, évitant le recours au style inline
 * avec des variables Django (incompatible avec les linters CSS).
 */

document.addEventListener('DOMContentLoaded', function () {
    /* Pour chaque élément portant data-animate-index, on calcule
       le délai d'animation : index × 100ms              */
    document.querySelectorAll('[data-animate-index]').forEach(function (el) {
        var index = parseInt(el.dataset.animateIndex, 10) || 0;
        el.style.animationDelay = (index * 100) + 'ms';
    });
});
