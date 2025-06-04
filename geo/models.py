from django.contrib.gis.db import models as geomodels

class Location(geomodels.Model):
    name = geomodels.CharField(max_length=100)
    point = geomodels.PointField(geography=True, null=True, blank=True)
    shape = geomodels.GeometryField(geography=True, null=True, blank=True)
    


    