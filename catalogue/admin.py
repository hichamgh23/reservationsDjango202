from django.contrib import admin
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
    # C'est cette ligne qui lie visuellement les artistes au show
    inlines = [ArtistTypeShowInline]

# 3. Config Réservations
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_show', 'places')
    
    def get_show(self, obj):
        return obj.representation.show.title
    get_show.short_description = 'Spectacle'

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

