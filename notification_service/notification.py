import redis
import threading
import json
import logging
import socketio
import eventlet
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

class WebSocketManager:
    def emit_fire_alert(self, detection_data: Dict[str, Any]):
        # Ensure field compatibility between different naming conventions
        camera_id = detection_data.get('camera_id') or detection_data.get('stream_id')
        
        alert_data = {
            'type': 'fire_detection',
            'camera_id': camera_id,
            'stream_id': camera_id,  # Add both for compatibility
            'camera_name': detection_data.get('camera_name') or detection_data.get('farm_id') or camera_id,
            'farm_id': detection_data.get('farm_id'),
            'confidence': detection_data.get('confidence'),
            'timestamp': detection_data.get('timestamp'),
            'detection_id': detection_data.get('detection_id'),
            'image_url': detection_data.get('image_url'),   # Add image URL if available
            'bounding_box': detection_data.get('bounding_box'),
            'source': detection_data.get('source', 'fire_detection')
        }
        
        sio.emit('fire_alert', alert_data)
        logger.info(f"🔥 Emitted fire alert for camera {alert_data['camera_id']} with confidence {alert_data['confidence']}%")

ws_manager = WebSocketManager()

@sio.event
def connect(sid, environ):
    logger.info(f"Client {sid} connected")

@sio.event
def disconnect(sid):
    logger.info(f"Client {sid} disconnected")

@sio.event
def ping(sid, data):
    logger.info(f"Ping from {sid}: {data}")
    sio.emit('pong', {'received': data, 'timestamp': time.time()}, room=sid)

@sio.event
def test_fire_alert(sid, data):
    logger.info(f"Test fire alert request from {sid}: {data}")
    # Emit a test response
    test_alert = {
        'type': 'fire_detection',
        'camera_id': 'websocket_test',
        'camera_name': 'WebSocket Test Camera',
        'confidence': 99.9,
        'timestamp': time.time(),
        'source': 'websocket_test'
    }
    sio.emit('fire_alert', test_alert, room=sid)

def redis_listener():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        pubsub = r.pubsub()
        pubsub.subscribe('fire_alerts')
        logger.info("📡 Subscribed to 'fire_alerts' Redis channel")

        for message in pubsub.listen():
            if message['type'] == 'message':
                try:
                    data = json.loads(message['data'])
                    logger.info(f"📨 Received fire alert: Camera {data.get('camera_id')}, Confidence: {data.get('confidence')}")
                    ws_manager.emit_fire_alert(data)
                except Exception as e:
                    logger.error(f"❌ Error processing Redis fire alert: {e}")
    except Exception as e:
        logger.error(f"❌ Fatal error in Redis listener: {e}")
        raise

# Start redis thread
def run_websocket_server(host='localhost', port=5001):
    try:
        redis_thread = threading.Thread(target=redis_listener, daemon=True)
        redis_thread.start()
        logger.info("🔁 Redis listener started")
        logger.info(f"🔌 Starting WebSocket server on {host}:{port}")
        eventlet.wsgi.server(eventlet.listen((host, port)), app)
    except Exception as e:
        logger.error(f"❌ Error starting WebSocket server: {e}")
        raise
import redis, json

r = redis.Redis()



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_websocket_server()

