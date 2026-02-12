from django.contrib import admin
from .models import Artist, Type, Locality, Role, Location, Show, Representation, ArtistType, ArtistTypeShow, Reservation

admin.site.site_header = "PICKSHOW PRO ADMIN"

class ProDesign(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# Appliquer ProDesign à CHAQUE enregistrement
admin.site.register(Show, ProDesign)
admin.site.register(Artist, ProDesign)
admin.site.register(Type, ProDesign)
admin.site.register(Locality, ProDesign)
admin.site.register(Role, ProDesign)
admin.site.register(Location, ProDesign)
admin.site.register(Representation, ProDesign)
admin.site.register(ArtistType, ProDesign)
admin.site.register(ArtistTypeShow, ProDesign)
admin.site.register(Reservation, ProDesign)

