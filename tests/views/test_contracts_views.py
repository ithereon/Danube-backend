from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from danube.accounts.models import User
from tests.factories import (
    ContractFactory,
    UserFactory,
    WorkItemFactory,
    BusinessDetailsFactory,
)


@pytest.mark.django_db
def test_create_contract(api_client, contract_dict):
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    property = contract_dict["property_obj"]
    business = BusinessDetailsFactory.create()
    contract_dict["business"] = business.id

    api_client.force_authenticate(customer_user)

    response = api_client.post(
        reverse(viewname="contracts:contract-list"), data=contract_dict, secure=True
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == contract_dict["title"]


@pytest.mark.django_db
def test_lists_contract_with_items(api_client):
    business_user = UserFactory.create(user_type=User.BUSINESS)
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    contract = ContractFactory.create(
        business__user=business_user, property_obj__user=customer_user
    )
    # ContractFactory.create_batch(10)
    work_item = WorkItemFactory.create(contract=contract)
    api_client.force_authenticate(business_user)

    response = api_client.get(reverse(viewname="contracts:contract-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == contract.id
    assert response.data["results"][0]["work_items"][0]["id"] == work_item.id

    api_client.force_authenticate(customer_user)

    response = api_client.get(reverse(viewname="contracts:contract-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == contract.id


@pytest.mark.django_db
@pytest.mark.skip
def test_lists_contract(api_client, work_item_dict):
    business_user = UserFactory.create(user_type=User.BUSINESS)
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    contract = ContractFactory.create(
        business__user=business_user, property_obj__user=customer_user
    )
    # ContractFactory.create_batch(10)
    api_client.force_authenticate(business_user)

    response = api_client.get(reverse(viewname="contracts:contract-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == contract.id

    api_client.force_authenticate(customer_user)

    response = api_client.get(reverse(viewname="contracts:contract-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == contract.id


@pytest.mark.django_db
@pytest.mark.skip
def test_lists_contract_total_cost(api_client):
    business_user = UserFactory.create(user_type=User.BUSINESS)
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    contract = ContractFactory.create(
        business__user=business_user, property_obj__user=customer_user
    )
    ContractFactory.create_batch(10)
    api_client.force_authenticate(business_user)

    # before creating work item, total should be 0
    response = api_client.get(reverse(viewname="contracts:contract-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == contract.id
    assert Decimal(response.data["results"][0]["total_cost"]) == Decimal(0)

    # after creating work item, total should be equal to work item price
    work_item = WorkItemFactory.create(contract=contract)
    response = api_client.get(reverse(viewname="contracts:contract-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == contract.id
    assert response.data["results"][0]["work_items"][0]["id"] == work_item.id
    assert Decimal(response.data["results"][0]["total_cost"]) == Decimal(response.data["results"][0]["work_items"][0]["price"])

    # after creating another work item, total cost should be sum
    work_item_2 = WorkItemFactory.create(contract=contract)
    response = api_client.get(reverse(viewname="contracts:contract-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == contract.id
    assert response.data["results"][0]["work_items"][0]["id"] == work_item_2.id
    assert Decimal(response.data["results"][0]["total_cost"]) == Decimal(response.data["results"][0]["work_items"][0]["price"]) + Decimal(response.data["results"][0]["work_items"][1]["price"])


@pytest.mark.django_db
def test_contract_costs(api_client):
    business_user = UserFactory.create(user_type=User.BUSINESS)
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        status=1
    )
    WorkItemFactory.create(contract=contract, price=500)

    api_client.force_authenticate(business_user)

    response = api_client.post(
        reverse(viewname="contracts:contract-costs", kwargs={"pk": contract.id}),
        data={
            "discount": 20,
            "discount_type": 2,
            "vat": 10,
            "first_payment": 100
        },
        secure=True
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == contract.id
    assert Decimal(response.data["vat"]) == Decimal(10)
    assert Decimal(response.data["discount"]) == Decimal(20)
    assert Decimal(response.data["first_payment_amount"]) == Decimal(100)
    assert response.data["discount_type"] == 2


@pytest.mark.django_db
@pytest.mark.skip
def test_contract_acceptance(api_client):
    business_user = UserFactory.create(user_type=User.BUSINESS)
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        status=1,
        first_payment_amount=200
    )
    api_client.force_authenticate(business_user)
    # business user sends contract to customer
    response = api_client.post(reverse(viewname="contracts:contract-send", kwargs={"pk": contract.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK

    api_client.force_authenticate(customer_user)
    # customer accepts sent contract
    response = api_client.post(reverse(viewname="contracts:contract-accept", kwargs={"pk": contract.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK

    # invoice is automatically created
    response = api_client.get(reverse(viewname="invoices:invoice-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["contract"]["id"] == contract.id


@pytest.mark.django_db
@pytest.mark.skip
def test_contract_complete_business(api_client):
    business_user = UserFactory.create(user_type=User.BUSINESS)
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        status=3
    )
    api_client.force_authenticate(business_user)
    # business user completes contract
    response = api_client.post(reverse(viewname="contracts:contract-complete", kwargs={"pk": contract.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK

    # invoice should be created after business completes contract
    response = api_client.get(reverse(viewname="invoices:invoice-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["contract"]["id"] == contract.id


@pytest.mark.django_db
@pytest.mark.skip
def test_contract_complete_customer(api_client):
    business_user = UserFactory.create(user_type=User.BUSINESS)
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        status=3
    )
    api_client.force_authenticate(customer_user)
    # customer user completes contract
    response = api_client.post(reverse(viewname="contracts:contract-complete", kwargs={"pk": contract.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK

    # invoice should NOT be created after customer completes contract
    response = api_client.get(reverse(viewname="invoices:invoice-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 0


@pytest.mark.django_db
@pytest.mark.skip
def test_contract_ordering(api_client):
    business_user = UserFactory.create(user_type=User.BUSINESS)
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        status=3
    )
    api_client.force_authenticate(customer_user)
    response = api_client.get(reverse(viewname="contracts:contract-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1

    newer_contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        status=3
    )

    response = api_client.get(reverse(viewname="contracts:contract-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["id"] == newer_contract.id

    newest_contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        status=3
    )

    response = api_client.get(reverse(viewname="contracts:contract-list"), follow=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 3
    assert response.data["results"][0]["id"] == newest_contract.id
    assert response.data["results"][1]["id"] == newer_contract.id
    assert response.data["results"][2]["id"] == contract.id
