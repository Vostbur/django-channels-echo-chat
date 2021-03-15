from django.urls import path

from .consumers import (
    ChatConsumer,
    ChatJsonConsumer
)


websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),
    path('ws/chat/<slug:room_name>/', ChatJsonConsumer.as_asgi()),
]
