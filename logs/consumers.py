import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class BuildConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'build_%s' % self.room_name