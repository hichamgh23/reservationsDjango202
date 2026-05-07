/**
 * cookies.js — Gestion du bandeau RGPD
 *
 * Affiche le bandeau si l'utilisateur n'a pas encore fait son choix.
 * Stocke la décision dans un cookie valable 1 an.
 */

function accepterCookies() {
    document.cookie = "cookies_accepted=true; max-age=" + (60 * 60 * 24 * 365) + "; path=/";
    document.getElementById('cookie-banner').style.display = 'none';
}

function refuserCookies() {
    document.cookie = "cookies_accepted=false; max-age=" + (60 * 60 * 24 * 365) + "; path=/";
    document.getElementById('cookie-banner').style.display = 'none';
}

/* Affiche le bandeau uniquement si aucun cookie de consentement n'existe */
document.addEventListener('DOMContentLoaded', function () {
    if (!document.cookie.includes('cookies_accepted')) {
        document.getElementById('cookie-banner').style.display = 'flex';
    }
});
