from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login,logout
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import GEOSGeometry
from .models import Location
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/login/')
def location(request):
    return render(request, 'Gis/map.html')


@csrf_exempt
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



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('location')  # Redirect to your map view
        else:
            return render(request, 'Gis/login.html', {'error': 'Invalid credentials'})
    return render(request, 'Gis/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            return render(request, 'Gis/register.html', {'error': 'Username already exists'})

        if password1 != password2:
            return render(request, 'Gis/register.html', {'error': 'Passwords do not match'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # Optional: make sure user is active
        user.is_active = True
        user.save()

        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('location')
        else:
            return render(request, 'Gis/register.html', {'error': 'Authentication failed after registration'})
    
    return render(request, 'Gis/register.html')
