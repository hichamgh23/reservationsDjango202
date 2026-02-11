from django.contrib import admin
from .models import Artist, Type, Locality, Role, Location, Show, Representation, ArtistType

admin.site.register(Artist)
admin.site.register(Type)
admin.site.register(Locality)
admin.site.register(Role)
admin.site.register(Location)
admin.site.register(Show)
admin.site.register(Representation)
admin.site.register(ArtistType)

