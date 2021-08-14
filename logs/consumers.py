import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import subprocess
from deployment.utils import run_command,cb
from deployment.deployActions.node import *



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
        await self.stream_logs()

    async def disconnect(self):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def stream_logs(self):
        process = subprocess.Popen(f"docker logs {self.room_name} --until 10m",stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if process.poll() is not None and output == b'':
                break
            if output:
                message = output.strip()
                # Send message to WebSocket
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'app_logs',
                        'message':message 
                    }
                )
        retval = process.poll()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'build_%s' % self.room_name
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        self.stream_logs()
    

    # Receive message from room group
    async def app_logs(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            "log_type":"application_log"
        }))
    
    # Receive message from room group
    async def build_logs(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            "log_type":"build_log"
        }))
    
    

