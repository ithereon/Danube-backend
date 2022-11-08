import pytest
from django.urls import reverse
from rest_framework import status

from danube.accounts.models import User
from tests.factories import (
    UserFactory,
    BusinessDetailsFactory,
    ChatRoomFactory,
    EOIFactory,
    RFQFactory,
    PropertyFactory,
)


@pytest.mark.django_db
def test_chat_exists(api_client):
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    business_user = UserFactory.create(user_type=User.BUSINESS)
    propert = PropertyFactory.create(user=customer_user)
    rfq = RFQFactory.create(property=propert)
    business = BusinessDetailsFactory.create(user=business_user)
    eoi = EOIFactory.create(business=business, rfq=rfq)
    chat = ChatRoomFactory.create(
        eoi=eoi,
        author=customer_user,
        participant=business_user
    )

    api_client.force_authenticate(customer_user)
    response = api_client.get(
        reverse(viewname="chat:chat_room_exist", kwargs={"participant_id": business_user.id}), follow=True
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_exists"] == True
    assert response.data["room"] == chat.id