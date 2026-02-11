from django.contrib import admin
from .models import Artist, Type, Locality, Role, Location, Show

admin.site.register(Artist)
admin.site.register(Type)
admin.site.register(Locality)
admin.site.register(Role)
admin.site.register(Location)
admin.site.register(Show)