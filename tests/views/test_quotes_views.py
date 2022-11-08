import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from danube.accounts.models import User
from danube.quotes.models import RFQ, RFQBusinessRequest, EOI
from tests.factories import (
    PropertyFactory,
    RFQFactory,
    RFQItemFactory,
    RFQBusinessRequestFactory,
    BusinessDetailsFactory,
    EOIFactory,
)


@pytest.mark.django_db
def test_create_rfq(rfq_dict):
    property_obj = PropertyFactory.create()
    rfq_dict["property"] = property_obj.id
    client = APIClient()
    client.force_authenticate(user=property_obj.user)
    response = client.post(reverse(viewname="quotes:rfq-list"), data=rfq_dict, secure=True)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == rfq_dict["title"]


@pytest.mark.django_db
def test_update_rfq():
    rfq = RFQFactory.create()
    new_title = "Test county"
    client = APIClient()
    client.force_authenticate(user=rfq.property.user)
    response = client.patch(
        reverse(viewname="quotes:rfq-detail", kwargs={"pk": rfq.id}),
        data={"title": new_title},
        secure=True
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == new_title


@pytest.mark.django_db
def test_get_rfq_list():
    property_obj = PropertyFactory.create()
    RFQFactory.create_batch(5)
    RFQFactory.create_batch(3, property=property_obj)
    client = APIClient()
    client.force_authenticate(user=property_obj.user)
    response = client.get(reverse(viewname="quotes:rfq-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3
    assert response.data["results"][0]["property"]["id"] == property_obj.id


@pytest.mark.django_db
def test_get_rfq_detail():
    property_obj = PropertyFactory.create()
    rfq = RFQFactory.create(property=property_obj)
    client = APIClient()
    client.force_authenticate(user=property_obj.user)
    response = client.get(reverse(viewname="quotes:rfq-detail", kwargs={"pk": rfq.id}), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == rfq.id


@pytest.mark.django_db
def test_create_rfq_item(rfq_item_dict):
    rfq = RFQFactory.create()
    rfq_item_dict["rfq"] = rfq.id
    client = APIClient()
    client.force_authenticate(user=rfq.property.user)
    response = client.post(
        reverse(viewname="quotes:rfq_items-list"), data=rfq_item_dict, secure=True
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["area_of_work"] == rfq_item_dict["area_of_work"]


@pytest.mark.django_db
def test_send_rfq():
    rfq = RFQFactory.create()
    rfq_item = RFQItemFactory.create(rfq=rfq)
    client = APIClient()
    client.force_authenticate(user=rfq.property.user)
    response = client.get(reverse(viewname="quotes:rfq-detail", kwargs={"pk": rfq.id}), follow=True)
    assert response.data["status"] == "SAVED"
    response_send = client.post(
        reverse(viewname="quotes:rfq-send", kwargs={"pk": rfq.id}), secure=True
    )
    assert response_send.status_code == status.HTTP_200_OK
    assert response_send.data == "RFQ was send."


@pytest.mark.django_db
def test_create_rfq_business(rfq_business_request_dict):
    rfq = RFQFactory.create()
    rfq_business_request_dict["rfq"] = rfq.id
    client = APIClient()
    user = rfq.property.user
    user.user_type = User.CUSTOMER
    user.save()
    client.force_authenticate(user=user)
    response = client.post(
        reverse(viewname="quotes:rfq_business-list"), data=rfq_business_request_dict, secure=True
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    RFQItemFactory.create(rfq=rfq)
    response = client.post(
        reverse(viewname="quotes:rfq_business-list"), data=rfq_business_request_dict, secure=True
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["rfq"]["id"] == rfq.id
    assert RFQ.objects.get(id=rfq.id).status == RFQ.PRIVATE


@pytest.mark.django_db
def test_get_rfq_business_list():
    rfq_business_request = RFQBusinessRequestFactory()
    RFQBusinessRequestFactory.create_batch(10)
    client = APIClient()
    business_user = rfq_business_request.business_profile.user
    business_user.user_type = User.BUSINESS
    business_user.save()
    client.force_authenticate(user=business_user)
    response = client.get(
        reverse(
            viewname="quotes:rfq_business-detail",
            kwargs={"pk": rfq_business_request.id},
        ),
        follow=True
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == rfq_business_request.id
    response = client.get(reverse(viewname="quotes:rfq_business-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == rfq_business_request.id
    customer_user = rfq_business_request.rfq.property.user
    customer_user.user_type = User.CUSTOMER
    customer_user.save()
    client.force_authenticate(user=customer_user)
    response = client.get(
        reverse(
            viewname="quotes:rfq_business-detail",
            kwargs={"pk": rfq_business_request.id},
        ),
        follow=True
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == rfq_business_request.id
    response = client.get(reverse(viewname="quotes:rfq_business-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == rfq_business_request.id


@pytest.mark.django_db
def test_rfq_business_request_decline():
    rfq_request = RFQBusinessRequestFactory.create()
    user = rfq_request.business_profile.user
    user.user_type = User.BUSINESS
    user.save()
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(
        reverse(viewname="quotes:rfq_business-decline", kwargs={"pk": rfq_request.id}),
        secure=True
    )
    assert response.status_code == status.HTTP_200_OK
    assert RFQBusinessRequest.objects.get(pk=rfq_request.id).status == 4


@pytest.mark.django_db
def test_create_eoi_open(eoi_dict):
    rfq = RFQFactory.create(status=3)
    business = BusinessDetailsFactory.create()
    eoi_dict["rfq"] = rfq.id
    eoi_dict["business"] = business.id
    client = APIClient()
    user = business.user
    user.user_type = User.EMPLOYEE
    user.save()
    client.force_authenticate(user=user)
    response = client.post(reverse(viewname="quotes:eoi-list"), data=eoi_dict, secure=True)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["rfq"]["id"] == rfq.id


@pytest.mark.django_db
def test_create_eoi_private(eoi_dict):
    rfq = RFQFactory.create(status=4)
    eoi_dict["rfq"] = rfq.id
    business = BusinessDetailsFactory.create()
    eoi_dict["business"] = business.id
    client = APIClient()
    user = business.user
    user.user_type = User.EMPLOYEE
    user.save()
    client.force_authenticate(user=user)
    response = client.post(reverse(viewname="quotes:eoi-list"), data=eoi_dict, secure=True)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # RFQ business is required for private RFQ's
    rfq_business = RFQBusinessRequestFactory.create(rfq=rfq, business_profile=business)
    response = client.post(reverse(viewname="quotes:eoi-list"), data=eoi_dict, secure=True)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["rfq"]["id"] == rfq.id


@pytest.mark.django_db
def test_get_eoi_list():
    eoi = EOIFactory.create()
    EOIFactory.create_batch(10)
    client = APIClient()
    business_user = eoi.business.user
    business_user.user_type = User.BUSINESS
    business_user.save()
    client.force_authenticate(user=business_user)
    response = client.get(reverse(viewname="quotes:eoi-detail", kwargs={"pk": eoi.id}), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == eoi.id
    response = client.get(reverse(viewname="quotes:eoi-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == eoi.id
    customer_user = eoi.rfq.property.user
    customer_user.user_type = User.CUSTOMER
    customer_user.save()
    client.force_authenticate(user=customer_user)
    response = client.get(reverse(viewname="quotes:eoi-detail", kwargs={"pk": eoi.id}), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == eoi.id
    response = client.get(reverse(viewname="quotes:eoi-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == eoi.id


@pytest.mark.django_db
def test_eoi_decline(base_client):
    eoi = EOIFactory.create()
    user = eoi.rfq.property.user
    user.user_type = User.CUSTOMER
    user.save()
    base_client.force_authenticate(user=user)
    response = base_client.post(
        reverse(viewname="quotes:eoi-decline", kwargs={"pk": eoi.id}),
        secure=True
    )
    assert response.status_code == status.HTTP_200_OK
    assert EOI.objects.get(pk=eoi.id).status == 3


@pytest.mark.django_db
@pytest.mark.skip
def test_business_rfq_open_or_private(base_client):
    rfq = RFQFactory(status=RFQ.OPEN)
    rfq_business_request = RFQBusinessRequestFactory(rfq__status=RFQ.OPEN)
    RFQBusinessRequestFactory.create_batch(10)
    client = APIClient()
    business_user = rfq_business_request.business_profile.user
    business_user.user_type = User.BUSINESS
    business_user.save()
    client.force_authenticate(user=business_user)
    response = client.get(
        '/rfq_business/getopenorprivate/?status=OPEN',
        follow=True
    )
    assert response.status_code == status.HTTP_200_OK