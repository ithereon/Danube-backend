from django.urls import path

from .views import ChatRoomListCreateAPIView, MessageListAPIView, CheckChatExistsView
app_name = "chat"
urlpatterns = [
    path("chats/", ChatRoomListCreateAPIView.as_view(), name="chat_list_create"),
    path(
        "chats/<int:chat_room_id>/messages/",
        MessageListAPIView.as_view(),
        name="chat_room_messages",
    ),
    path(
        "chats/<int:participant_id>/exists/",
        CheckChatExistsView.as_view(),
        name="chat_room_exist",
    ),
]
