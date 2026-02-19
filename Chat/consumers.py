import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        user = self.scope["user"]

        # Reject if not authenticated
        if user.is_anonymous:
            print(f"WebSocket REJECTED: User is anonymous. Cookies: {self.scope.get('cookies')}")
            await self.close()
            return

        # Check if user belongs to room
        if not await self.is_user_in_room(user):
            print(f"WebSocket REJECTED: User '{user}' is not a member of room '{self.room_id}'")
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message", "").strip()
        except json.JSONDecodeError:
            print("WebSocket ERROR: Received invalid JSON")
            return

        user = self.scope["user"]

        # Ignore empty messages
        if not message:
            return

        timestamp = await self.save_message(user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": user.username,
                "timestamp": timestamp,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "timestamp": event["timestamp"],
        }))

    @database_sync_to_async
    def save_message(self, user, message):
        msg = Message.objects.create(
            room_id=self.room_id,
            user=user,
            content=message
        )
        return msg.created_at.isoformat()

    @database_sync_to_async
    def is_user_in_room(self, user):
        return Room.objects.filter(id=self.room_id, users=user).exists()