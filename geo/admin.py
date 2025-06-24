from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location

class LocationAdmin(LeafletGeoAdmin):
    list_display = ('name',)
    # Optionally, you can set default map view:
    default_lon = 33.892166
    default_lat = 9.561555499999997
    default_zoom = 2

admin.site.register(Location, LocationAdmin)
