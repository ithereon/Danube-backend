import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories import ChatRoomFactory


@pytest.mark.django_db
def test_chat_search(client_customer, customer):
    chat1 = ChatRoomFactory.create(participant__last_name="FIRST", author=customer)
    ChatRoomFactory.create(participant__last_name="FIRST")
    ChatRoomFactory.create(participant__last_name="SECOND", author=customer)
    response = client_customer.get(reverse("chat:chat_list_create"), data={"search": "first"}, follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["id"] == chat1.id