from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import GEOSGeometry
from .models import Location
import os
from django.conf import settings


def location(request):
    return render(request, 'Gis/map.html')


def save_geojson(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        features = data.get('features', [])
        name = data.get('name', 'Drawn Shape')

        # Save GeoJSON to a local file
        geojson_dir = os.path.join(settings.BASE_DIR, 'geojson_files')
        os.makedirs(geojson_dir, exist_ok=True)
        filename = f"{name.replace(' ', '_')}.geojson"
        filepath = os.path.join(geojson_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Save to database as before
        for feature in features:
            geom = GEOSGeometry(json.dumps(feature['geometry']))
            Location.objects.create(
                name=name,
                point=geom if geom.geom_type == 'Point' else None,
                shape=geom if geom.geom_type != 'Point' else None
            )
        return JsonResponse({'message': 'Data saved!'})
    return JsonResponse({'message': 'Invalid request'}, status=400)
