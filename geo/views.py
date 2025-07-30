from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import GEOSGeometry
from .models import Location
from cams.models import Camera, FireDetection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import traceback
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta


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
        camera_id = data.get('camera_id', '').strip()

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
                    camera_id=camera_id,
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

# =============================================================================
# FIRE DETECTION VIEWS - Real-time Alert Management
# =============================================================================

@csrf_exempt
async def fire_alert_webhook(request):
    """
    Webhook endpoint to receive fire detection alerts from the detection service.
    Expected JSON format:
    {
        "camera_id": "CAM-001",
        "farm_id": "FARM-A", 
        "confidence": 0.92,
        "timestamp": "2025-01-29T10:30:00Z",
        "image_data": "base64_encoded_image",
        "bounding_box": {"x": 100, "y": 50, "width": 200, "height": 150}
    }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        body = request.body
        data = await sync_to_async(json.loads)(body)
        
        # Validate required fields
        required_fields = ['camera_id', 'confidence']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
        
        # Create fire detection record
        fire_detection = await sync_to_async(FireDetection.objects.create)(
            camera_id=data.get('camera_id'),
            farm_id=data.get('farm_id', 'Unknown'),
            confidence=float(data.get('confidence')),
            timestamp=timezone.now(),
            image_data=data.get('image_data'),
            bounding_box=data.get('bounding_box'),
            notes=data.get('notes', '')
        )
        
        # Return success response
        return JsonResponse({
            'status': 'success',
            'message': 'Fire alert recorded successfully',
            'alert_id': fire_detection.id,
            'timestamp': fire_detection.timestamp.isoformat()
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': f'Invalid data: {str(e)}'}, status=400)
    except Exception as e:
        print(f"Fire alert webhook error: {str(e)}")
        traceback.print_exc()
        return JsonResponse({'error': 'Internal server error'}, status=500)

@login_required(login_url='/login/')
async def get_fire_alerts(request):
    """
    API endpoint to fetch fire alerts with filtering and pagination.
    Query parameters:
    - status: all, active, resolved
    - priority: all, high, medium, low  
    - time_range: all, 1h, 24h, 7d
    - page: page number for pagination
    - limit: items per page (default 20)
    """
    try:
        # Get query parameters
        status = request.GET.get('status', 'all')
        priority = request.GET.get('priority', 'all')
        time_range = request.GET.get('time_range', 'all')
        page = int(request.GET.get('page', 1))
        limit = min(int(request.GET.get('limit', 20)), 100)  # Max 100 items per page
        
        # Build query
        query = Q()
        
        # Filter by status
        if status == 'active':
            query &= Q(is_resolved=False)
        elif status == 'resolved':
            query &= Q(is_resolved=True)
        
        # Filter by priority (based on confidence)
        if priority == 'critical':
            query &= Q(confidence__gte=0.9)
        elif priority == 'high':
            query &= Q(confidence__gte=0.7, confidence__lt=0.9)
        elif priority == 'medium':
            query &= Q(confidence__gte=0.5, confidence__lt=0.7)
        elif priority == 'low':
            query &= Q(confidence__lt=0.5)
        
        # Filter by time range
        if time_range != 'all':
            now = timezone.now()
            if time_range == '1h':
                cutoff = now - timedelta(hours=1)
            elif time_range == '24h':
                cutoff = now - timedelta(hours=24)
            elif time_range == '7d':
                cutoff = now - timedelta(days=7)
            else:
                cutoff = None
            
            if cutoff:
                query &= Q(timestamp__gte=cutoff)
        
        # Get alerts with pagination
        alerts_queryset = FireDetection.objects.filter(query).order_by('-timestamp')
        
        # Wrap pagination in sync_to_async
        paginator = Paginator(alerts_queryset, limit)
        alerts_page = await sync_to_async(paginator.get_page)(page)
        alerts_list = await sync_to_async(list)(alerts_page)
        
        # Format alerts for JSON response
        alerts_data = []
        for alert in alerts_list:
            alerts_data.append({
                'id': alert.id,
                'camera_id': alert.camera_id,
                'farm_id': alert.farm_id,
                'confidence': alert.confidence,
                'timestamp': alert.timestamp.isoformat(),
                'is_resolved': alert.is_resolved,
                'severity_level': alert.severity_level,
                'image_url': alert.image_url,
                'bounding_box': alert.bounding_box,
                'notes': alert.notes
            })
        
        # Get statistics
        total_alerts = await sync_to_async(FireDetection.objects.count)()
        active_alerts = await sync_to_async(FireDetection.objects.filter(is_resolved=False).count)()
        resolved_alerts = await sync_to_async(FireDetection.objects.filter(is_resolved=True).count)()
        
        return JsonResponse({
            'status': 'success',
            'alerts': alerts_data,
            'pagination': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_next': alerts_page.has_next(),
                'has_previous': alerts_page.has_previous()
            },
            'statistics': {
                'total_alerts': total_alerts,
                'active_alerts': active_alerts,
                'resolved_alerts': resolved_alerts
            }
        })
        
    except Exception as e:
        print(f"Get fire alerts error: {str(e)}")
        traceback.print_exc()
        return JsonResponse({'error': 'Failed to fetch alerts'}, status=500)

@csrf_exempt
@login_required(login_url='/login/')
async def resolve_fire_alert(request, alert_id):
    """
    Mark a fire alert as resolved.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        # Get the alert
        alert = await sync_to_async(get_object_or_404)(FireDetection, id=alert_id)
        
        # Parse request body for notes
        body = request.body
        if body:
            data = await sync_to_async(json.loads)(body)
            notes = data.get('notes', '')
            if notes:
                alert.notes = notes
        
        # Mark as resolved
        alert.is_resolved = True
        await sync_to_async(alert.save)()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Alert resolved successfully',
            'alert_id': alert.id
        })
        
    except Exception as e:
        print(f"Resolve alert error: {str(e)}")
        return JsonResponse({'error': 'Failed to resolve alert'}, status=500)

@csrf_exempt
@login_required(login_url='/login/')
async def delete_fire_alert(request, alert_id):
    """
    Delete a fire alert.
    """
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)
    
    try:
        # Get the alert
        alert = await sync_to_async(get_object_or_404)(FireDetection, id=alert_id)
        
        # Delete the alert
        await sync_to_async(alert.delete)()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Alert deleted successfully'
        })
        
    except Exception as e:
        print(f"Delete alert error: {str(e)}")
        return JsonResponse({'error': 'Failed to delete alert'}, status=500)

@csrf_exempt
@login_required(login_url='/login/')
async def bulk_resolve_alerts(request):
    """
    Resolve multiple alerts at once.
    Expected JSON: {"alert_ids": [1, 2, 3], "notes": "Resolved by admin"}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        body = request.body
        data = await sync_to_async(json.loads)(body)
        
        alert_ids = data.get('alert_ids', [])
        notes = data.get('notes', '')
        
        if not alert_ids:
            return JsonResponse({'error': 'No alert IDs provided'}, status=400)
        
        # Update alerts
        updated_count = await sync_to_async(
            FireDetection.objects.filter(id__in=alert_ids).update
        )(is_resolved=True, notes=notes)
        
        return JsonResponse({
            'status': 'success',
            'message': f'{updated_count} alerts resolved successfully'
        })
        
    except Exception as e:
        print(f"Bulk resolve error: {str(e)}")
        return JsonResponse({'error': 'Failed to resolve alerts'}, status=500)

@login_required(login_url='/login/')
async def export_fire_alerts(request):
    """
    Export fire alerts as JSON.
    """
    try:
        # Get query parameters for filtering
        status = request.GET.get('status', 'all')
        time_range = request.GET.get('time_range', 'all')
        
        # Build query
        query = Q()
        
        if status == 'active':
            query &= Q(is_resolved=False)
        elif status == 'resolved':
            query &= Q(is_resolved=True)
        
        if time_range != 'all':
            now = timezone.now()
            if time_range == '1h':
                cutoff = now - timedelta(hours=1)
            elif time_range == '24h':
                cutoff = now - timedelta(hours=24)
            elif time_range == '7d':
                cutoff = now - timedelta(days=7)
            else:
                cutoff = None
            
            if cutoff:
                query &= Q(timestamp__gte=cutoff)
        
        # Get alerts
        alerts_queryset = FireDetection.objects.filter(query).order_by('-timestamp')
        alerts_list = await sync_to_async(list)(alerts_queryset)
        
        # Format for export
        export_data = {
            'export_timestamp': timezone.now().isoformat(),
            'total_alerts': len(alerts_list),
            'filters': {
                'status': status,
                'time_range': time_range
            },
            'alerts': []
        }
        
        for alert in alerts_list:
            export_data['alerts'].append({
                'id': alert.id,
                'camera_id': alert.camera_id,
                'farm_id': alert.farm_id,
                'confidence': alert.confidence,
                'timestamp': alert.timestamp.isoformat(),
                'is_resolved': alert.is_resolved,
                'severity_level': alert.severity_level,
                'notes': alert.notes,
                'bounding_box': alert.bounding_box
            })
        
        # Create response
        response = JsonResponse(export_data, json_dumps_params={'indent': 2})
        filename = f"fire_alerts_{timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        print(f"Export alerts error: {str(e)}")
        return JsonResponse({'error': 'Failed to export alerts'}, status=500)

@login_required(login_url='/login/')
async def fire_alerts_dashboard(request):
    """
    Render the fire alerts dashboard page.
    """
    # Get recent alerts for initial display
    recent_alerts = await sync_to_async(
        lambda: list(FireDetection.objects.order_by('-timestamp')[:10])
    )()
    
    # Get statistics
    total_alerts = await sync_to_async(FireDetection.objects.count)()
    active_alerts = await sync_to_async(FireDetection.objects.filter(is_resolved=False).count)()
    resolved_alerts = await sync_to_async(FireDetection.objects.filter(is_resolved=True).count)()
    
    context = {
        'recent_alerts': recent_alerts,
        'statistics': {
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'resolved_alerts': resolved_alerts
        }
    }
    
    return await sync_to_async(render)(request, 'Gis/fire_alerts_dashboard.html', context)

@login_required(login_url='/login/')
async def alert_demo_view(request):
    """
    Render the alert manager demo page.
    """
    return await sync_to_async(render)(request, 'Gis/alert_demo.html')