import time
import json

from django.core.management.base import BaseCommand

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Command(BaseCommand):
    def handle(self, *args, **options):
        channel_layer = get_channel_layer()

        for i in range(10):
            content = json.dumps({
                "message": f"Message {i} outside of consumer"
            })
            async_to_sync(channel_layer.group_send)(
                "room",  # ws://127.0.0.1:8000/ws/chat/room/
                {"type": "chat.message", "content": content},
            )
            time.sleep(1)