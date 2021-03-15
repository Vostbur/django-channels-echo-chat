Django channels training project
--------------------------------

URL to echo service:

`ws://127.0.0.1:8000/ws/chat/`

URL to chat room service:

`ws://127.0.0.1:8000/ws/chat/any_chat_room_name/`

Test sending message outside of consumers:

`python manage.py message_test`

on URL

`ws://127.0.0.1:8000/ws/chat/room/`
