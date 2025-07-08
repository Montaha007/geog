from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import GEOSGeometry
from .models import Location
from cams.models import Camera
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import traceback


@login_required(login_url='/login/')
async def location(request):
    # Use sync_to_async for ORM query
    user_location = await sync_to_async(
        lambda: list(Location.objects.filter(user=request.user))
    )()

    location_json = {}
    for loc in user_location:
        point_coords = [loc.point.y, loc.point.x] if loc.point else None
        # Accessing .geojson property might trigger a synchronous operation, wrap it
        shape_geojson = await sync_to_async(
            lambda: loc.shape.geojson if loc.shape else None
        )()
        shape_coords = json.loads(shape_geojson)['coordinates'] if shape_geojson else None

        location_json[loc.id] = {
            'name': loc.name,
            'point': point_coords,
            'shape': shape_coords
        }

    return await sync_to_async(render)(request, 'Gis/map.html', {
        'user_location': user_location,
        'location_json': json.dumps(location_json)
    })

@csrf_exempt
async def save_geojson(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid request'}, status=400)

    # ✅ Safely get the user object
    user = await sync_to_async(lambda: request.user)()
    is_authenticated = await sync_to_async(lambda: user.is_authenticated)()
    if not is_authenticated:
        return JsonResponse({'message': 'Authentication required'}, status=401)

    try:
    # ✅ FIXED: do NOT await request.body
        body = request.body

    # ✅ still wrap json.loads, since it's CPU-bound
        data = await sync_to_async(json.loads)(body)


        features = data.get('features', [])
        name = data.get('name', 'Drawn Shape')
        rtsp = data.get('rtsp', '').strip()
        stream_id = data.get('stream_id', '').strip()

        if not features:
            return JsonResponse({'message': 'No features found in request.'}, status=400)

        for feature in features:
            geometry = feature.get('geometry')
            if not geometry:
                continue

            # ✅ wrap GEOSGeometry creation
            geom = await sync_to_async(GEOSGeometry)(json.dumps(geometry))

            # ✅ ORM create (wrapped)
            location = await sync_to_async(Location.objects.create)(
                name=name,
                point=geom if geom.geom_type == 'Point' else None,
                shape=geom if geom.geom_type != 'Point' else None,
                user=user
            )

            if rtsp:
                await sync_to_async(Camera.objects.create)(
                    stream_id=stream_id,
                    rtsp_url=rtsp,
                    location=location
                )

        return JsonResponse({'message': 'Location and camera saved successfully!'})

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON.'}, status=400)
    

    except Exception as e:
    # Log the full traceback in the console
        print("🔥 FULL ERROR TRACEBACK 🔥")
        traceback.print_exc()

    # Return the actual error string to the browser
        return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    await channel_layer.group_send("map_updates", update_data)

async def history_view(request):
    # Wrap ORM query
    hist = await sync_to_async(
        lambda: list(Location.objects.filter(user=request.user)
                     .order_by('-created_at')
                     .prefetch_related('cameras'))
    )()
    return await sync_to_async(render)(request, 'Gis/history.html', {'history': hist})

async def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Wrap authenticate
        user = await sync_to_async(authenticate)(request, username=username, password=password)
        if user is not None:
            # Wrap login
            await sync_to_async(login)(request, user)
            return redirect('location')
        else:
            return await sync_to_async(render)(request, 'Gis/logins/login.html', {'error': 'Invalid credentials'})
    return await sync_to_async(render)(request, 'Gis/logins/login.html')

async def logout_view(request):
    if request.method == 'POST':
        # Wrap logout
        await sync_to_async(logout)(request)
        return redirect('login')
    # If not POST, just redirect to login (or return an error)
    return redirect('login') # Or render an error page

async def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Wrap ORM query
        username_exists = await sync_to_async(User.objects.filter(username=username).exists)()
        if username_exists:
            return await sync_to_async(render)(request, 'Gis/logins/register.html', {'error': 'Username already exists'})
        if password1 != password2:
            return await sync_to_async(render)(request, 'Gis/logins/register.html', {'error': 'Passwords do not match'})
        
        # Wrap ORM create_user
        user = await sync_to_async(User.objects.create_user)(username=username, email=email, password=password1)
        
        # Wrap user.save()
        user.is_active = True
        await sync_to_async(user.save)()

        # Wrap authenticate and login
        user = await sync_to_async(authenticate)(request, username=username, password=password1)
        if user is not None:
            await sync_to_async(login)(request, user)
            return redirect('location')
        else:
            return await sync_to_async(render)(request, 'Gis/logins/register.html', {'error': 'Authentication failed after registration'})
    return await sync_to_async(render)(request, 'Gis/logins/register.html')


async def download_location(request, pk):
    # Wrap get_object_or_404
    loc = await sync_to_async(get_object_or_404)(Location, pk=pk)

    geojson = '{}'
    if loc.shape:
        # Wrap access to .geojson
        geojson = await sync_to_async(lambda: loc.shape.geojson)()
    elif loc.point:
        # Wrap access to .geojson
        geojson = await sync_to_async(lambda: loc.point.geojson)()

    response = HttpResponse(geojson, content_type='application/geo+json')
    response['Content-Disposition'] = f'attachment; filename="{loc.name}.geojson"'
    return response

async def delete_location(request, pk):
    # Wrap get_object_or_404
    loc = await sync_to_async(get_object_or_404)(Location, pk=pk)
    if request.method == 'POST':
        # Wrap delete operation
        await sync_to_async(loc.delete)()
        return redirect('history')
    return redirect('history') # If not POST, just redirect