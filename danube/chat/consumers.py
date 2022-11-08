from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from rest_framework.generics import get_object_or_404

from .services import MessageService

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        try:
            user = User.objects.get(id=data["user_id"])
        except (User.DoesNotExist, KeyError):
            self.disconnect(close_code="Invalid user_id")

        message = MessageService.create(
            content=data["message"], author=user, chat_room_id=data["chat_id"],
        )
        content = {
            "command": "new_message",
            "message": self.message_to_json(message=message),
        }
        return self.send_chat_message(content)

    def send_typing_signal(self, data):
        content = {"command": "send_typing_signal", "message": data}
        return self.send_chat_message(content)

    @staticmethod
    def message_to_json(message):
        return {
            "id": message.id,
            "author": {
                "id": message.author.id,
                "first_name": message.author.first_name,
                "last_name": message.author.last_name,
            },
            "content": message.content,
            "timestamp": str(message.created_at),
        }

    commands = {"new_message": new_message, "send_typing_signal": send_typing_signal}

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))
