import json

from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import login, logout
from channels.db import database_sync_to_async

from .models import Online


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        message = json_data["message"]

        await self.send(text_data=json.dumps({"message": message}))


class ChatJsonConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.create_online()
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        user = await self.get_user_from_db()
        await login(self.scope, user)
        await database_sync_to_async(self.scope['session'].save)()

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        self.scope['session']['my_var'] = 'hello from session'
        await database_sync_to_async(self.scope['session'].save)()
        await self.accept()

    async def disconnect(self, code):
        await logout(self.scope)
        await database_sync_to_async(self.scope['session'].save)()
        await self.delete_online()
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(
            self.room_name, {"type": "chat.message", "content": content}
        )
        await self.refresh_online()
        await self.channel_layer.group_send(
            self.room_name, 
            {
                "type": "chat.message", 
                "content": f"{str(self.online)}\
                     {self.scope['session']['my_var']}\
                          {self.scope['user'].email}"
            }
        )

    async def chat_message(self, event):
        await self.send_json(event["content"])

    @database_sync_to_async
    def create_online(self):
        self.online, _ = Online.objects.get_or_create(name=self.channel_name)

    @database_sync_to_async
    def delete_online(self):
        Online.objects.filter(name=self.channel_name).delete()

    @database_sync_to_async
    def refresh_online(self):
        self.online.refresh_from_db()

    @database_sync_to_async
    def get_user_from_db(self):
        return get_user_model().objects.filter(email='admin@admin.com').first()
