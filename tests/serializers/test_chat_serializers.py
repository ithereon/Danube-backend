import pytest

from danube.chat.serializers import ChatRoomCreateSerializer


@pytest.mark.django_db
def test_chat_room_serializer(chat_room_dict):
    serializer = ChatRoomCreateSerializer(data=chat_room_dict)
    assert serializer.is_valid()
