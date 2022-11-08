from django.contrib.auth import get_user_model
from django.db import models

from danube.quotes.models import EOI

User = get_user_model()


class ChatRoom(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="chat_room_author"
    )
    participant = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="chat_room_participant"
    )
    eoi = models.OneToOneField(
        EOI, on_delete=models.CASCADE, null=True, blank=True, related_name="chat_room"
    )
    new_from_author = models.BooleanField(default=False)
    new_from_participant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{getattr(self.author, "name", "")} <-> {getattr(self.participant, "name", "")}'

    class Meta:
        unique_together = ("author", "participant", "eoi")


class Message(models.Model):
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.SET_NULL, null=True, related_name="messages"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return getattr(self.author, "email", "")
