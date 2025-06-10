from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import User
class Location(geomodels.Model):
    name = geomodels.CharField(max_length=100)
    point = geomodels.PointField(geography=True, null=True, blank=True)
    shape = geomodels.GeometryField(geography=True, null=True, blank=True)
    created_at = geomodels.DateTimeField(auto_now_add=True)
    updated_at = geomodels.DateTimeField(auto_now=True)
    user = geomodels.ForeignKey(User, on_delete=geomodels.CASCADE, related_name='locations')  # Add this line
    
    def __str__(self):
        return self.name



    