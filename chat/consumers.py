import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        message = json_data['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))


class ChatJsonConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat.message',
                'content': content
            }
        )

    async def chat_message(self, event):
        await self.send_json(event['content'])
