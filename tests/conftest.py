import json

import django
import pytest
from django.forms import model_to_dict
from faker import Faker
from rest_framework.test import APIClient

from danube import settings


def pytest_configure():
    """Configure pytest."""
    settings.DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    settings.AWS_S3_ENDPOINT_URL = "127.0.0.1:8000"
    settings.SITE_URL = "127.0.0.1:8000"
    settings.FCM_TOKEN = "123456789"
    settings.FRONT_URL = "127.0.0.1:8000"
    django.setup()


@pytest.fixture()
def faker():
    return Faker()


@pytest.fixture()
def customer():
    from tests.factories import UserFactory

    return UserFactory.create(user_type=1)


@pytest.fixture()
def business():
    from tests.factories import UserFactory

    return UserFactory.create(user_type=2)


@pytest.fixture()
def employee():
    from tests.factories import UserFactory

    return UserFactory.create(user_type=3)


@pytest.fixture()
def client_customer(customer):
    """Get API client."""
    client = APIClient()
    client.force_authenticate(user=customer)
    return client


@pytest.fixture()
def base_client():
    """Get API client."""
    return APIClient()


@pytest.fixture()
def api_client():
    """API client to auth."""
    return APIClient()


@pytest.fixture()
def client_business(business):
    """Get API client."""
    client = APIClient()
    client.force_authenticate(user=business)
    return client


@pytest.fixture()
def client_employee(employee):
    """Get API client."""
    client = APIClient()
    client.force_authenticate(user=employee)
    return client


@pytest.fixture()
def property_dict():
    from tests.factories import PropertyFactory

    property = PropertyFactory.build()
    return model_to_dict(property)


@pytest.fixture()
def business_details_dict():
    from tests.factories import BusinessDetailsFactory

    business_details = BusinessDetailsFactory.build()
    return model_to_dict(business_details)


@pytest.fixture()
def rfq_dict():
    from tests.factories import RFQFactory
    from tests.factories import PropertyFactory

    rfq = RFQFactory.build()
    obj_dict = model_to_dict(rfq)
    obj_dict["property"] = PropertyFactory.create().id
    return obj_dict


@pytest.fixture()
def rfq_item_dict():
    from tests.factories import RFQItemFactory

    rfq_item = RFQItemFactory.build()
    obj_dict = model_to_dict(rfq_item)
    obj_dict["rfq"] = rfq_item.rfq.id
    return model_to_dict(rfq_item)


@pytest.fixture()
def rfq_business_request_dict():
    from tests.factories import (
        RFQBusinessRequestFactory,
        RFQFactory,
        BusinessDetailsFactory,
    )

    business_request = RFQBusinessRequestFactory.build()
    obj_dict = model_to_dict(business_request)
    rfq = RFQFactory.create()
    business = BusinessDetailsFactory.create()
    obj_dict["rfq"] = rfq.id
    obj_dict["business_profile"] = business.id
    obj_dict.pop("id")
    return obj_dict


@pytest.fixture()
def eoi_dict():
    from tests.factories import (
        RFQFactory,
        BusinessDetailsFactory,
        EOIFactory,
    )

    eoi = EOIFactory.build()
    obj_dict = model_to_dict(eoi)
    rfq = RFQFactory.create(status=3)
    business = BusinessDetailsFactory.create()
    obj_dict["rfq"] = rfq.id
    obj_dict["business"] = business.id
    obj_dict.pop("id")
    return obj_dict


@pytest.fixture()
def contract_dict():
    from tests.factories import (
        ContractFactory,
        BusinessDetailsFactory,
        EOIFactory,
        PropertyFactory,
    )

    contract = ContractFactory.build()
    obj_dict = model_to_dict(contract)
    business = BusinessDetailsFactory.create()
    property_obj = PropertyFactory.create()
    eoi = EOIFactory.create(business=business)
    obj_dict["business"] = business.id
    obj_dict["property_obj"] = property_obj.id
    obj_dict["eoi"] = eoi.id
    obj_dict.pop("id")
    return obj_dict


@pytest.fixture()
def work_item_dict():
    from tests.factories import WorkItemFactory, ContractFactory

    work_item = WorkItemFactory.build()
    obj_dict = model_to_dict(work_item)
    contract = ContractFactory.create()
    obj_dict["contract"] = contract.id
    obj_dict.pop("id")
    return obj_dict


@pytest.fixture()
def chat_room_dict():
    from tests.factories import UserFactory, ChatRoomFactory, EOIFactory
    obj = ChatRoomFactory.build()
    obj_dict = model_to_dict(obj)
    author = UserFactory.create()
    participant = UserFactory.create()
    eoi = EOIFactory.create(rfq__property__user=author, business__user=participant)
    obj_dict["author_id"] = author.id
    obj_dict["participant_id"] = participant.id
    obj_dict["eoi"] = eoi.id
    obj_dict["message"] = "Test message"
    return obj_dict


@pytest.fixture()
def message_create_dict():
    from tests.factories import UserFactory, ChatRoomFactory, MessageFactory
    obj = MessageFactory.build()
    obj_dict = model_to_dict(obj)
    obj_dict["author"] = UserFactory.create().id
    obj_dict["chat_id"] = ChatRoomFactory.create().id
    obj_dict["command"] = "new_message"
    return obj_dict


@pytest.fixture()
def invoice_dict():
    from tests.factories import (
        InvoiceFactory,
        BusinessDetailsFactory,
        EOIFactory,
        PropertyFactory,
        ContractFactory,
    )

    invoice = InvoiceFactory.build()
    obj_dict = model_to_dict(invoice)
    contract = ContractFactory.create()
    business = BusinessDetailsFactory.create()
    property_obj = PropertyFactory.create()
    eoi = EOIFactory.create(business=business)
    obj_dict["business"] = business.id
    obj_dict["property_obj"] = property_obj.id
    obj_dict["eoi"] = eoi.id
    # obj_dict["contract_id"] = contract.id
    obj_dict["contract"] = contract.id
    obj_dict.pop("id")
    return obj_dict
