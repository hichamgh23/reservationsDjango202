from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import csv
from django.http import HttpResponse
from decimal import Decimal
from .models import (
    Artist, Type, Locality, Role, Location, Show, 
    Representation, Reservation, Profile, ArtistType, ArtistTypeShow
)

# 1. Inline pour les artistes du spectacle
class ArtistTypeShowInline(admin.TabularInline):
    model = ArtistTypeShow
    extra = 1
    verbose_name = "Artiste du spectacle"
    verbose_name_plural = "Artistes participant à ce spectacle"

# 2. Show
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'bookable', 'voir_site')
    list_filter = ('bookable',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArtistTypeShowInline]

    def voir_site(self, obj):
        return format_html('<a href="/show/{}/" target="_blank" class="button">Voir sur le site</a>', obj.id)
    voir_site.short_description = 'Action'

# 3. Reservation avec export CSV
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_show', 'places')
    actions = ['export_as_csv']
    
    def get_show(self, obj):
        return obj.representation.show.title
    get_show.short_description = 'Spectacle'

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reservations.csv"'
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['ID', 'Utilisateur', 'Email', 'Spectacle', 'Date', 'Lieu', 'Places', 'Total'])
        for res in queryset.select_related('user', 'representation__show', 'representation__location'):
            total = res.places * res.representation.show.price + Decimal('2.00')
            writer.writerow([
                res.id, res.user.username, res.user.email,
                res.representation.show.title,
                res.representation.when.strftime('%d/%m/%Y %H:%M'),
                res.representation.location.designation if res.representation.location else '-',
                res.places, total
            ])
        return response
    export_as_csv.short_description = "Exporter les réservations sélectionnées en CSV"

# 4. Artist
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'voir_site')
    search_fields = ('firstname', 'lastname')

    def voir_site(self, obj):
        return format_html('<a href="/artist/{}/" target="_blank" class="button">Voir sur le site</a>', obj.id)
    voir_site.short_description = 'Action'

# 5. Location
class LocationAdmin(admin.ModelAdmin):
    list_display = ('designation', 'address', 'locality', 'voir_site')
    search_fields = ('designation', 'address')

    def voir_site(self, obj):
        return format_html('<a href="/location/{}/" target="_blank" class="button">Voir sur le site</a>', obj.id)
    voir_site.short_description = 'Action'

# 6. Locality
class LocalityAdmin(admin.ModelAdmin):
    list_display = ('postal_code', 'locality', 'voir_liste')
    search_fields = ('postal_code', 'locality')

    def voir_liste(self, obj):
        return mark_safe('<a href="/localities/" target="_blank" class="button">Voir la liste</a>')
    voir_liste.short_description = 'Action'

# Enregistrement
models_configs = {
    Show: ShowAdmin,
    Reservation: ReservationAdmin,
    Artist: ArtistAdmin,
    Location: LocationAdmin,
    Locality: LocalityAdmin,
}

for model, admin_class in models_configs.items():
    if admin.site.is_registered(model):
        admin.site.unregister(model)
    admin.site.register(model, admin_class)

other_models = [Type, Role, Representation, Profile, ArtistType, ArtistTypeShow]

for model in other_models:
    if not admin.site.is_registered(model):
        admin.site.register(model)
