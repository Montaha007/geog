import redis
import json
import logging
import os
import sys
import time
from typing import Dict, Any
from datetime import datetime

# Add Django setup for database access
import django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Import your fire detection model and WebSocket manager
from cams.models import FireDetection
logger = logging.getLogger(__name__)

class FireAlertListener:
    """
    Listens for fire detection alerts from Redis and handles them
    """
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=0):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.pubsub = self.redis_client.pubsub()
        self.is_listening = False
        
    def start_listening(self):
        """Start listening for fire alerts"""
        try:
            self.pubsub.subscribe('fire_alerts')
            self.is_listening = True
            logger.info("🔥 Started listening for fire alerts...")
            
            # Use get_message with timeout to make it interruptible
            while self.is_listening:
                try:
                    message = self.pubsub.get_message(timeout=1.0)
                    if message is None:
                        continue
                        
                    if message['type'] == 'message':
                        try:
                            alert_data = json.loads(message['data'].decode('utf-8'))
                            self.handle_fire_alert(alert_data)
                        except Exception as e:
                            logger.error(f"Error processing fire alert: {e}")
                            
                except Exception as e:
                    logger.error(f"Error getting message from Redis: {e}")
                    if self.is_listening:
                        time.sleep(1)  # Brief pause before retrying
                        
        except Exception as e:
            logger.error(f"Error in fire alert listener: {e}")
        finally:
            try:
                self.pubsub.close()
                logger.info("Fire alert listener pubsub closed")
            except Exception as e:
                logger.error(f"Error closing pubsub: {e}")
            
    def handle_fire_alert(self, alert_data: Dict[str, Any]):
        """Handle a fire detection alert"""
        camera_id = alert_data.get('camera_id')
        timestamp = alert_data.get('timestamp')
        confidence = alert_data.get('confidence', 0.0)
        farm_id = alert_data.get('farm_id', '')
        camera_name = alert_data.get('name', f'Camera {camera_id}')
        
        logger.warning(f"🚨 FIRE DETECTED! Camera: {camera_id}, Time: {timestamp}, Confidence: {confidence}")
        print(f"🚨 FIRE ALERT: {alert_data}")
        
        # Save to your fire detection model
        try:
            detection = FireDetection.objects.create(
                camera_id=camera_id,
                farm_id=farm_id,
                confidence=confidence,
                image_data=alert_data.get('image_data'),  # Save base64 image data
                bounding_box=alert_data.get('bounding_box')
                # You can add image_path if you want to link to the frame
            )
            logger.info(f"✅ Fire detection saved to database: ID {detection.id}")
            
   
        except Exception as e:
            logger.error(f"❌ Failed to save fire detection to database: {e}")
        
        # Additional emergency actions
        self.trigger_emergency_actions(alert_data, detection if 'detection' in locals() else None)
        
    def trigger_emergency_actions(self, alert_data: Dict[str, Any], detection=None):
        """Trigger additional emergency protocols"""
        try:
            camera_id = alert_data.get('camera_id')
            confidence = alert_data.get('confidence', 0.0)
            
            # High confidence fire detection - trigger immediate alerts
            if confidence >= 80.0:
                logger.critical(f"🚨 HIGH CONFIDENCE FIRE DETECTED ({confidence}%) - Camera {camera_id}")
                
                # You can add:
                # - Email notifications
                # - SMS alerts
                # - Emergency service notifications
                # - Automatic sprinkler activation
                # - Sound alarms
                
            # Log all fire detections for audit trail
            logger.warning(f"Fire detection logged: Camera {camera_id}, Confidence: {confidence}%")
            
        except Exception as e:
            logger.error(f"Error in emergency actions: {e}")
        
    def stop_listening(self):
        """Stop listening for fire alerts"""
        self.is_listening = False
        logger.info("Stopped listening for fire alerts")