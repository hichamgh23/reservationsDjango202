from django.contrib import admin
from .models import Artist, Type, Locality, Role, Location, Show, Representation, Reservation, ArtistType, ArtistTypeShow

# Configuration pour les Lieux (Source 320)
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('designation', 'locality', 'capacity', 'phone')
    search_fields = ('designation', 'locality__locality')
    prepopulated_fields = {'slug': ('designation',)}

# Configuration pour les Spectacles (Source 348)
@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'bookable', 'location')
    list_filter = ('bookable', 'location')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

# Configuration pour les Représentations (Source 306)
@admin.register(Representation)
class RepresentationAdmin(admin.ModelAdmin):
    list_display = ('show', 'when', 'location')
    list_filter = ('when', 'show')

# Configuration pour les Réservations (Source 8)
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'representation', 'places')
    list_filter = ('user', 'representation__show')

# Enregistrement simple pour les autres modèles
admin.site.register(Artist)
admin.site.register(Type)
admin.site.register(Locality)
admin.site.register(Role)
admin.site.register(ArtistType)
admin.site.register(ArtistTypeShow)

