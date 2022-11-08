from django.contrib.auth import get_user_model
from django.db.models import DateField
from django.db.models import OuterRef
from django.db.models import Subquery
from django.db.models import Value
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from danube.chat.models import ChatRoom
from danube.chat.models import Message
from .serializers import ChatRoomCreateSerializer
from .serializers import ChatRoomListSerializer
from .serializers import MessageListSerializer
from .services import ChatRoomService
from .services import MessageService
from ..quotes.models import EOI

User = get_user_model()


class ChatRoomListCreateAPIView(ListCreateAPIView):
    serializer_class = ChatRoomListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        SearchFilter,
    )
    search_fields = [
        "author__first_name",
        "participant__first_name",
        "author__last_name",
        "participant__last_name",
        "participant__username",
        "author__username",
    ]

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, args, kwargs)
    #     chat_list = ChatRoomService.get_user_eoi_chat_rooms_with_sub_queries(
    #         user=self.request.user
    #     )
    #     response.data["chat_list"] = self.serializer_class(
    #         chat_list, many=True, context={"user": request.user}
    #     ).data
    #     response.data["chat_list_total_count"] = chat_list.count()
    #     return response

    def get_queryset(self):
        latest_message = (
            Message.objects.filter(chat_room=OuterRef("id"))
            .order_by("-created_at")
            .values("created_at")[:1]
        )
        return (
            ChatRoomService.get_user_chat_rooms(user=self.request.user)
            .annotate(
                _latest_message=Subquery(latest_message),
                latest_message=Coalesce(
                    "_latest_message",
                    Value("1970-01-01T00:00:00Z"),
                    output_field=DateField(),
                ),
            )
            .order_by("-latest_message")
        )

    def create(self, request, *args, **kwargs):
        serializer = ChatRoomCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        author_id = serializer.validated_data.get("author_id")
        participant_id = serializer.validated_data.get("participant_id")
        eoi_id = serializer.validated_data.get("eoi")
        message = serializer.validated_data.get("message", None)

        user_a = get_object_or_404(User, id=author_id)
        user_b = get_object_or_404(User, id=participant_id)
        eoi = get_object_or_404(EOI, id=eoi_id)
        author = user_a
        participant = user_b
        if user_a.is_employee:
            participant = user_a
            author = user_b
        if ChatRoomService.has_already_created(author=author, participant=participant):
            chat_room = ChatRoomService.get(
                author=author, participant=participant, eoi=eoi
            )
        else:
            chat_room = ChatRoomService.create(
                author=author, participant=participant, eoi=eoi
            )

            if message:
                MessageService.create(
                    content=message, author=user_a, chat_room_id=chat_room.id,
                )

        return Response(
            ChatRoomListSerializer(chat_room).data, status=status.HTTP_200_OK
        )

    def get_serializer_context(self):
        if self.request:
            return {"request": self.request, "user": self.request.user}


class MessageListAPIView(ListAPIView):
    serializer_class = MessageListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        SearchFilter,
    )
    search_fields = [
        "content"
    ]

    def get_queryset(self):
        chat_room_id = self.kwargs.get("chat_room_id")
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        if self.request.user == chat_room.author:
            chat_room.new_from_participant = False
            chat_room.author_notified_via_email = False
        else:
            chat_room.new_from_author = False
            chat_room.participant_notified_via_email = False
        chat_room.save()
        return MessageService.get_user_messages_by_chat_id(chat_room_id=chat_room_id)


class CheckChatExistsView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, participant_id, *args, **kwargs):
        participant = get_object_or_404(User, id=participant_id)
        author = request.user
        if ChatRoomService.has_already_created(
                author=author, participant=participant
        ) or ChatRoomService.has_already_created(
            author=participant, participant=author
        ):
            room = ChatRoom.objects.get(participant=participant, author=author)
            return Response({"is_exists": True, "room": room.id}, status=status.HTTP_200_OK)
        else:
            return Response({"is_exists": False}, status=status.HTTP_200_OK)
