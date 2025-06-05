from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import GEOSGeometry
from .models import Location

def location(request):
    return render(request, 'Gis/map.html')

def save_geojson(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        features = data.get('features', [])
        name = data.get('name', 'Drawn Shape')
        for feature in features:
            geom = GEOSGeometry(json.dumps(feature['geometry']))
            Location.objects.create(
                name=name,
                point=geom if geom.geom_type == 'Point' else None,
                shape=geom if geom.geom_type != 'Point' else None
            )
        return JsonResponse({'message': 'Data saved!'})
    return JsonResponse({'message': 'Invalid request'}, status=400)

