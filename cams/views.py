from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from asgiref.sync import sync_to_async
import traceback # Import traceback for better error logging

from .models import Camera
from geo.models import Location # Assuming 'geo' is the app where Location model resides

# Helper functions to wrap synchronous ORM calls for async views
# This makes your async views cleaner by defining these once
aget_object_or_404 = sync_to_async(get_object_or_404)
acreate_camera = sync_to_async(Camera.objects.create)
arecord_clip = sync_to_async(lambda camera, duration: camera.record_clip(duration))


@login_required
async def add_camera(request, location_id):
    # Synchronous access to request.method and request.POST is generally fine
    # within an async view as it's not a long-running I/O operation.
    if request.method == 'POST':
        name = request.POST.get('name')
        stream_id = request.POST.get('stream_id')

        # Basic validation
        if not name or not stream_id:
            # Using JsonResponse for API-like feedback, even if redirecting later
            return JsonResponse({'status': 'error', 'message': 'Missing name or stream_id'}, status=400)

        try:
            # Use await with the async helper for get_object_or_404
            # Add security: Ensure the location belongs to the current user
            location = await aget_object_or_404(Location.objects.filter(user=request.user), id=location_id)
            
            # Use await with the async helper for create
            await acreate_camera(name=name, stream_id=stream_id, location=location)

            # Redirects are synchronous, so wrap render/redirect if they become complex
            # For simple redirects, it's often acceptable to leave as is or wrap
            return await sync_to_async(redirect)('location') # Redirect to your actual map or success view
        except Location.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Location not found or unauthorized.'}, status=404)
        except Exception as e:
            # Log the full traceback for debugging
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
    
    # If not POST, redirect immediately
    return await sync_to_async(redirect)('location') # fallback


@login_required
async def record_view(request, camera_id):
    try:
        # Use await with the async helper for get_object_or_404
        # Add security: Ensure the camera belongs to the current user's locations
        camera = await aget_object_or_404(Camera.objects.filter(location__user=request.user), pk=camera_id)
        
        # Use await with the async helper for the blocking record_clip method
        output_path = await arecord_clip(camera, duration=10)
        
        return JsonResponse({"status": "started", "path": output_path})
    except Camera.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Camera not found or unauthorized."}, status=404)
    except Exception as e:
        # Log the full traceback for debugging
        traceback.print_exc()
        return JsonResponse({"status": "error", "message": f"Failed to record clip: {str(e)}"}, status=500)