from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Camera
from geo.models import Location

@login_required
def add_camera(request, location_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        stream_id = request.POST.get('stream_id')

        location = get_object_or_404(Location, id=location_id)
        Camera.objects.create(name=name, stream_id=stream_id, location=location)

        return redirect('location')  # change to your actual map or success view

    return redirect('location')  # fallback
