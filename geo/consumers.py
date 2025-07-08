import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MapConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # You can send an initial message if needed
        await self.send(text_data=json.dumps({
            'message': 'Connected to the map WebSocket'
        }))

    async def disconnect(self, close_code):
        # Handle disconnection if needed
        await self.close()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            # Example: echo the received data back to the client
            await self.send(text_data=json.dumps({
                'message': f'Received: {data}'
            }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON received'
            }))