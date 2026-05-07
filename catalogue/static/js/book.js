/**
 * book.js — Calcul dynamique du total sur la page de réservation
 *
 * Lit le prix unitaire et les frais admin depuis l'attribut data-* du
 * conteneur #booking-data (injecté dans le template via Django).
 * Met à jour les champs #subtotal-places et #total-display en temps réel.
 */

$(document).ready(function () {
    var bookingData = document.getElementById('booking-data');
    if (!bookingData) return;

    var unitPrice = parseFloat(bookingData.dataset.price) || 0;
    var adminFees = parseFloat(bookingData.dataset.fees)  || 2.00;

    function updateTotal() {
        var qty = parseInt($('#places').val(), 10);
        if (isNaN(qty) || qty < 1) qty = 0;

        var sub   = unitPrice * qty;
        var total = (qty > 0) ? (sub + adminFees) : 0;

        $('#subtotal-places').text(sub.toFixed(2).replace('.', ','));
        $('#total-display').text(total.toFixed(2).replace('.', ','));
    }

    $('#places').on('input change', updateTotal);
    updateTotal(); /* Calcul initial dès le chargement */
});
