from rest_framework import serializers

from danube.accounts.serializers import UserSerializer
from danube.chat.models import ChatRoom, Message


class ChatRoomListSerializer(serializers.ModelSerializer):
    participant = serializers.SerializerMethodField()
    is_new_message = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    eoi = serializers.StringRelatedField()

    class Meta:
        model = ChatRoom
        fields = [
            "id",
            "participant",
            "eoi",
            "is_new_message",
            "last_message"
        ]

    def get_participant(self, chat_room):
        user = self.context.get("user")

        if chat_room.participant == user:
            return UserSerializer(chat_room.author).data
        return UserSerializer(chat_room.participant).data

    def get_is_new_message(self, chat_room):
        user = self.context.get("user")

        if chat_room.participant == user:
            return chat_room.new_from_author
        return chat_room.new_from_participant
    def get_last_message(self, chat_room):
        last_message = chat_room.messages.order_by("-created_at").first()
        if last_message:
            return MessageListSerializer(last_message).data



class ChatRoomCreateSerializer(serializers.Serializer):
    author_id = serializers.IntegerField(required=True)
    participant_id = serializers.IntegerField(required=True)
    eoi = serializers.IntegerField(required=True)
    message = serializers.CharField(required=True, allow_null=True)


class MessageListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    timestamp = serializers.DateTimeField(source="created_at")

    class Meta:
        model = Message
        fields = (
            "id",
            "author",
            "content",
            "timestamp",
        )
