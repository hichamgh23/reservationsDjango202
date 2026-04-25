from django.contrib import admin
import csv
from django.http import HttpResponse
from decimal import Decimal
from .models import (
    Artist, Type, Locality, Role, Location, Show, 
    Representation, Reservation, Profile, ArtistType, ArtistTypeShow
)

# 1. Configuration de l'Inline (Le tableau des artistes dans le spectacle)
class ArtistTypeShowInline(admin.TabularInline):
    model = ArtistTypeShow
    extra = 1
    verbose_name = "Artiste du spectacle"
    verbose_name_plural = "Artistes participant à ce spectacle"

# 2. Config Spectacles avec Inlines
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'bookable')
    list_filter = ('bookable',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArtistTypeShowInline]

# 3. Config Réservations avec export CSV
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
                res.id,
                res.user.username,
                res.user.email,
                res.representation.show.title,
                res.representation.when.strftime('%d/%m/%Y %H:%M'),
                res.representation.location.designation if res.representation.location else '-',
                res.places,
                total
            ])
        return response
    export_as_csv.short_description = "Exporter les réservations sélectionnées en CSV"

# Nettoyage et enregistrement sécurisé
models_configs = {
    Show: ShowAdmin,
    Reservation: ReservationAdmin,
}

# On enregistre les modèles avec config
for model, admin_class in models_configs.items():
    if admin.site.is_registered(model):
        admin.site.unregister(model)
    admin.site.register(model, admin_class)

# On enregistre le reste sans config spécifique
other_models = [
    Artist, Type, Locality, Role, Location, 
    Representation, Profile, ArtistType
]

for model in other_models:
    if not admin.site.is_registered(model):
        admin.site.register(model)
