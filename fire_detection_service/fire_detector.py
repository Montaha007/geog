from celery import Celery
from ultralytics import YOLO
import base64, json, redis, numpy as np, cv2
import os
from datetime import datetime

app = Celery('fire_detector', broker='redis://localhost:6379/0')

# Get the correct path for the YOLO model
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'best.pt')

# Check if model file exists
if not os.path.exists(model_path):
    print(f"❌ YOLO model file not found at: {model_path}")
    print("Please ensure 'best.pt' is in the fire_detection_service directory")
    model = None
else:
    print(f"✅ Loading YOLO model from: {model_path}")
    model = YOLO(model_path)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def publish_fire_alert(detection_data):
    """Publish fire alert to Redis channel"""
    try:
        redis_client.publish('fire_alerts', json.dumps(detection_data))
        print(f"📢 Published fire alert to Redis channel")
    except Exception as e:
        print(f"❌ Error publishing to Redis: {e}")

# Celery task - runs asynchronously
@app.task
def detect_fire_task(frame_b64, camera_id, name):
    if model is None:
        return "Model not loaded - check best.pt file"
    
    try:
        frame = cv2.imdecode(np.frombuffer(base64.b64decode(frame_b64), np.uint8), cv2.IMREAD_COLOR)
        results = model(frame)
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    label = model.names[int(box.cls)]
                    confidence = float(box.conf)
                    print(f"🔍 Detection: {label} (confidence: {confidence:.2f})")
                    
                    if label == "fire" and confidence > 0.5:  # Add confidence threshold
                        annotated_frame = result.plot()
                        
                        # Convert annotated frame to base64
                        _, buffer = cv2.imencode('.jpg', annotated_frame)
                        image_b64 = base64.b64encode(buffer).decode('utf-8')
                        
                        detection_data = {
                            "label": "fire",
                            "camera_id": camera_id,
                            "farm_id": name,
                            "confidence": confidence,
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                            "image_data": image_b64,
                            "bounding_box": {
                                "x1": float(box.xyxy[0][0]),
                                "y1": float(box.xyxy[0][1]), 
                                "x2": float(box.xyxy[0][2]),
                                "y2": float(box.xyxy[0][3])
                            }
                        }
                        
                        # Publish to Redis channel
                        publish_fire_alert(detection_data)
                        print(f"🚨 FIRE DETECTED! Camera: {camera_id}, Confidence: {confidence:.2f}")
                        return f"Fire detected with confidence {confidence:.2f}"
        
        return "No fire detected"
        
    except Exception as e:
        print(f"❌ Error in fire detection: {e}")
        return f"Error: {str(e)}"