/**
 * welcome.js — Animation du rideau de théâtre (page d'accueil)
 *
 * Ajoute la classe CSS 'opened' au conteneur du théâtre après 500ms,
 * ce qui déclenche l'animation d'ouverture des rideaux via les transitions CSS.
 */

window.addEventListener('load', function () {
    setTimeout(function () {
        var viewport = document.querySelector('.theater-viewport');
        if (viewport) {
            viewport.classList.add('opened');
        }
    }, 500);
});
