from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CameraConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "camera_updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({
            "status": "connected",
            "message": "Camera WebSocket connected"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Message from frontend:", data)

    async def send_camera_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))


# ✅ Add this class below it:
class DetectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("🔥 Fire detection received:", data)

        # You can broadcast to a group, or forward to the frontend here
        await self.send(text_data=json.dumps({
            "type": "detection",
            "payload": data
        }))
