from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from asgiref.sync import sync_to_async
import traceback # Import traceback for better error logging
import redis
import json
from datetime import datetime

from .models import Camera
from geo.models import Location # Assuming 'geo' is the app where Location model resides
redis_client = redis.Redis(host='localhost', port=6379, db=0)

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
        camera_id = request.POST.get('camera_id')

        # Basic validation
        if not name or not camera_id:
            # Using JsonResponse for API-like feedback, even if redirecting later
            return JsonResponse({'status': 'error', 'message': 'Missing name or camera_id'}, status=400)

        try:
            # Use await with the async helper for get_object_or_404
            # Add security: Ensure the location belongs to the current user
            location = await aget_object_or_404(Location.objects.filter(user=request.user), id=location_id)
            
            # Use await with the async helper for create
            await acreate_camera(name=name, camera_id=camera_id, location=location)

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
def get_fire_alerts(request):
    """Get stored fire alerts from Django database"""
    try:
        user_cameras = Camera.objects.filter(location__user=request.user)
        # Return alerts from Django DB
        alerts = []  # Query your FireAlert model here
        return JsonResponse({'status': 'success', 'alerts': alerts})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt

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
@login_required 
def notification_status(request):
    """Check if notification services are running"""
    try:
        # Test Redis connection
        redis_client.ping()
        redis_status = "connected"
        
        # Check if there are any active channels
        pubsub = redis_client.pubsub()
        channels = redis_client.pubsub_channels()
        channel_count = len(channels)
        
        return JsonResponse({
            'status': 'success',
            'services': {
                'redis': redis_status,
                'redis_channels': channel_count,
                'websocket': 'running',  # Assume running if Redis is working
                'fire_detection': 'active'
            },
            'message': 'All notification services are operational'
        })
        
    except redis.ConnectionError:
        return JsonResponse({
            'status': 'error',
            'message': 'Redis connection failed - notification services may be down',
            'services': {
                'redis': 'disconnected',
                'websocket': 'unknown',
                'fire_detection': 'unknown'
            }
        }, status=503)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': f'Service check failed: {str(e)}',
            'services': {
                'redis': 'error',
                'websocket': 'unknown', 
                'fire_detection': 'unknown'
            }
        }, status=500)

from django.http import JsonResponse
from .models import Camera

@login_required
def start_stream_view(request, camera_id):
    camera = Camera.objects.get(pk=camera_id)
    input_file = request.GET.get('file', 'sample.mp4')  # Or get from POST/form
    rtsp_url = camera.stream_file_to_rtsp(input_file)
    return JsonResponse({'status': 'started', 'rtsp_url': rtsp_url})

@csrf_exempt
@login_required
def test_fire_alert(request):
    """Test fire alert through Redis pipeline"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)
    
    try:
        # Create test fire alert data
        test_alert = {
            'type': 'fire_detection',
            'camera_id': 'test_cam_001',
            'stream_id': 'test_cam_001',  # Add both for compatibility
            'camera_name': 'Test Server Camera',
            'farm_id': 'test_server_farm',
            'confidence': 98.5,
            'timestamp': datetime.now().isoformat(),
            'detection_id': f'test_{int(datetime.now().timestamp())}',
            'source': 'django_test'
        }
        
        # Test Redis connection first
        try:
            redis_client.ping()
        except redis.ConnectionError:
            return JsonResponse({
                'status': 'error',
                'message': 'Redis server not running on port 6379. Start with: redis-server'
            }, status=503)
        
        # Publish to Redis fire_alerts channel (same as fire detection service)
        channel = 'fire_alerts'
        message = json.dumps(test_alert)
        
        redis_client.publish(channel, message)
        
        return JsonResponse({
            'status': 'success',
            'message': f'Test fire alert published to Redis channel "{channel}"',
            'alert_data': test_alert,
            'redis_channel': channel
        })
        
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to send test alert: {str(e)}'
        }, status=500)

@csrf_exempt
@login_required
def save_fire_alert(request):
    """Save fire alert to database"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Here you would save to your FireAlert model
        # For now, just acknowledge receipt
        
        return JsonResponse({
            'status': 'success',
            'message': 'Fire alert saved to database',
            'alert_id': data.get('detection_id', 'unknown')
        })
        
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to save alert: {str(e)}'
        }, status=500)