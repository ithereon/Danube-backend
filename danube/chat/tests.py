import pytz
from datetime import datetime
from unittest.mock import MagicMock

from django.test import TestCase

from danube.chat.models import Message, ChatRoom
from danube.chat.services import MessageService
from danube.accounts.models import User


class TestService(TestCase):
    def test_get_previous_message(self):
        user = User.objects.create_user("test@test.com", "my_password")
        first_message = Message.objects.create(content="content", author=user)
        second_message = Message.objects.create(content="content", author=user)
        Message.objects.create(
            content="content",
            author=user,
            chat_room=ChatRoom.objects.create(author=user),
        )
        message = MessageService.get_previous_message(message=first_message)
        self.assertEqual(message, second_message)

    def test_get_previous_message_empty_message(self):
        user = User.objects.create_user("test@test.com", "my_password")
        first_message = Message.objects.create(content="content", author=user)
        message = MessageService.get_previous_message(message=first_message)
        self.assertIsNone(message)
