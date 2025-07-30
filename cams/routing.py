from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/cam/', consumers.CameraConsumer.as_asgi()),           # 🎥 existing
    path('ws/detections/', consumers.DetectionConsumer.as_asgi())  # 🔥 new
]
