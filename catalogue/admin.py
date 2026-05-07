"""
admin.py — Configuration de l'interface d'administration Django

Fonctionnalités personnalisées :
    - ShowAdmin      : inline artistes + lien vers la page publique
    - ReservationAdmin : affichage du spectacle + export CSV par sélection
    - ArtistAdmin    : recherche + lien vers la page publique
    - LocationAdmin  : recherche + lien vers la page publique
    - LocalityAdmin  : recherche + lien vers la liste publique
"""

import csv
from decimal import Decimal

from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (
    Artist, ArtistType, ArtistTypeShow,
    Location, Locality, Profile,
    Representation, Reservation,
    Review, Role, Show, Type,
)


# ─────────────────────────────────────────────
# INLINES
# ─────────────────────────────────────────────

class ArtistTypeShowInline(admin.TabularInline):
    """Permet d'associer des artistes à un spectacle depuis la page Show."""
    model                = ArtistTypeShow
    extra                = 1
    verbose_name         = "Artiste du spectacle"
    verbose_name_plural  = "Artistes participant à ce spectacle"


# ─────────────────────────────────────────────
# CLASSES D'ADMINISTRATION PERSONNALISÉES
# ─────────────────────────────────────────────

class ShowAdmin(admin.ModelAdmin):
    """Administration des spectacles avec gestion inline des artistes."""
    list_display       = ('title', 'price', 'bookable', 'voir_site')
    list_filter        = ('bookable',)
    search_fields      = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines            = [ArtistTypeShowInline]

    def voir_site(self, obj):
        return format_html(
            '<a href="/show/{}/" target="_blank" class="button">Voir sur le site</a>',
            obj.id,
        )
    voir_site.short_description = 'Action'


class ReservationAdmin(admin.ModelAdmin):
    """Administration des réservations avec colonne spectacle et export CSV."""
    list_display = ('user', 'get_show', 'places')
    actions      = ['export_as_csv']

    def get_show(self, obj):
        return obj.representation.show.title
    get_show.short_description = 'Spectacle'

    def export_as_csv(self, request, queryset):  # noqa: ARG002 — signature imposée par Django admin
        """Action admin : exporte la sélection en fichier CSV (séparateur ;)."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reservations.csv"'
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['ID', 'Utilisateur', 'Email', 'Spectacle', 'Date', 'Lieu', 'Places', 'Total'])

        for res in queryset.select_related('user', 'representation__show', 'representation__location'):
            total = res.places * res.representation.show.price + Decimal('2.00')
            writer.writerow([
                res.id,
                res.user.username,
                res.user.email,
                res.representation.show.title,
                res.representation.when.strftime('%d/%m/%Y %H:%M'),
                res.representation.location.designation if res.representation.location else '-',
                res.places,
                total,
            ])
        return response
    export_as_csv.short_description = "Exporter les réservations sélectionnées en CSV"


class ArtistAdmin(admin.ModelAdmin):
    """Administration des artistes avec recherche et lien vers le site."""
    list_display  = ('firstname', 'lastname', 'voir_site')
    search_fields = ('firstname', 'lastname')

    def voir_site(self, obj):
        return format_html(
            '<a href="/artist/{}/" target="_blank" class="button">Voir sur le site</a>',
            obj.id,
        )
    voir_site.short_description = 'Action'


class LocationAdmin(admin.ModelAdmin):
    """Administration des lieux avec recherche et lien vers le site."""
    list_display  = ('designation', 'address', 'locality', 'voir_site')
    search_fields = ('designation', 'address')

    def voir_site(self, obj):
        return format_html(
            '<a href="/location/{}/" target="_blank" class="button">Voir sur le site</a>',
            obj.id,
        )
    voir_site.short_description = 'Action'


class LocalityAdmin(admin.ModelAdmin):
    """Administration des localités avec recherche et lien vers la liste publique."""
    list_display  = ('postal_code', 'locality', 'voir_liste')
    search_fields = ('postal_code', 'locality')

    def voir_liste(self, obj):  # noqa: Django admin display signature
        return mark_safe('<a href="/localities/" target="_blank" class="button">Voir la liste</a>')
    voir_liste.short_description = 'Action'


# ─────────────────────────────────────────────
# ENREGISTREMENT DES MODÈLES
# ─────────────────────────────────────────────

# Modèles avec classe d'administration personnalisée
_custom_admins = {
    Show:        ShowAdmin,
    Reservation: ReservationAdmin,
    Artist:      ArtistAdmin,
    Location:    LocationAdmin,
    Locality:    LocalityAdmin,
}

for model, admin_class in _custom_admins.items():
    if admin.site.is_registered(model):
        admin.site.unregister(model)
    admin.site.register(model, admin_class)

# Modèles enregistrés avec l'interface par défaut
_default_models = [Type, Role, Representation, Profile, ArtistType, ArtistTypeShow, Review]

for model in _default_models:
    if not admin.site.is_registered(model):
        admin.site.register(model)
