import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer



class BuildConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'build_%s' % self.room_name
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def build_message(self):
        message = 'Hi there, your logs are as follows'

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))