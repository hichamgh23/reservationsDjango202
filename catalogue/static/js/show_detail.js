/**
 * show_detail.js — Formulaire de réservation (page détail spectacle)
 *
 * Avant soumission du formulaire, récupère l'ID de la séance sélectionnée
 * et remplace le placeholder '0' dans l'URL d'action par le vrai ID.
 * Bloque la soumission si aucune séance n'est choisie.
 */

document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('utickBookingForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        var select = document.getElementById('repSelect');
        var repId  = select ? select.value : '';

        if (!repId) {
            e.preventDefault();
            alert('Veuillez sélectionner une séance avant de continuer.');
            return;
        }

        /* Remplace le '0' dans l'URL d'action par l'ID réel de la représentation */
        var actionUrl = this.getAttribute('action');
        this.action   = actionUrl.replace('/0/', '/' + repId + '/');
    });
});
