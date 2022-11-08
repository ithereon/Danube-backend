import pytest
from django.urls import reverse
from rest_framework import status

from danube.accounts.models import User
from tests.factories import (
    UserFactory,
    PropertyFactory,
    BusinessDetailsFactory
)


@pytest.mark.django_db
def test_create_user(faker, base_client):
    response = base_client.post(
        reverse(viewname="api-register"),
        data={
            "email": faker.email(),
            "password": "NSDhvsdjk1",
            "username": "test123",
            "password2": "NSDhvsdjk1",
            "usertype": "Customer",
        },
        secure=True
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_business(faker, base_client):
    response = base_client.post(
        reverse(viewname="api-register"),
        data={
            "email": faker.email(),
            "password": "NSDhvsdjk1",
            "username": "business",
            "password2": "NSDhvsdjk1",
            "usertype": "Business",
        },
        secure=True
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_employee_forbidden(faker, base_client):
    response = base_client.post(
        reverse(viewname="api-register"),
        data={
            "email": faker.email(),
            "password": "NSDhvsdjk1",
            "username": "employee",
            "password2": "NSDhvsdjk1",
            "usertype": "Employee",
        },
        secure=True
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_user_info(client_customer, customer):
    response = client_customer.get(
        reverse(
            viewname="users-details",
            kwargs={"pk": customer.id}
        ),
        follow=True
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == customer.id


@pytest.mark.django_db
def test_change_customer_property_info(base_client, faker):
    # after creating property is_property_created should be true for customer

    customer = User.objects.create_user(
        user_type=User.CUSTOMER,
        password="NSDhvsdjk1",
        email=faker.email(),
        username=faker.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        is_superuser=False,
        is_active=True
    )
    response = base_client.post(
        reverse(
            viewname="api-login"
        ),
        data={
            "email": customer.email,
            "password": "NSDhvsdjk1"
        },
        secure=True
    )
    # fresh customer user created, is_property_created should be false
    assert response.status_code == status.HTTP_200_OK
    assert not response.data["user"]["is_property_created"]

    PropertyFactory.create(user=customer)
    response = base_client.post(
        reverse(
            viewname="api-login"
        ),
        data={
            "email": customer.email,
            "password": "NSDhvsdjk1"
        },
        secure=True
    )
    # property is created, is_property_created should be true
    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"]["is_property_created"]

@pytest.mark.django_db
def test_change_business_user_property_info(base_client, faker):
    # after creating property is_property_created should be true for business

    business_user = User.objects.create_user(
        user_type=User.BUSINESS,
        password="NSDhvsdjk1",
        email=faker.email(),
        username=faker.user_name(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        is_superuser=False,
        is_active=True
    )
    response = base_client.post(
        reverse(
            viewname="api-login"
        ),
        data={
            "email": business_user.email,
            "password": "NSDhvsdjk1"
        },
        secure=True
    )
    # fresh business user created, is_property_created should be false
    assert response.status_code == status.HTTP_200_OK
    assert not response.data["user"]["is_property_created"]

    BusinessDetailsFactory.create(user=business_user)
    response = base_client.post(
        reverse(
            viewname="api-login"
        ),
        data={
            "email": business_user.email,
            "password": "NSDhvsdjk1"
        },
        secure=True
    )
    # business property is created, is_property_created should be true
    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"]["is_property_created"]

