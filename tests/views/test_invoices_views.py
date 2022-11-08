import pytest
from django.urls import reverse
from rest_framework import status

from danube.accounts.models import User
from danube.contracts.models import Contract
from danube.invoices.models import Invoice
from tests.factories import (
    ContractFactory,
    UserFactory,
    BusinessDetailsFactory,
    InvoiceFactory,
)


@pytest.mark.django_db
def test_create_invoice(api_client, invoice_dict):
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    business = BusinessDetailsFactory.create()
    invoice_dict["business"] = business.id

    api_client.force_authenticate(customer_user)

    response = api_client.post(
        reverse(viewname="invoices:invoice-list"), data=invoice_dict, secure=True
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == 'OPEN'
    assert response.data["status_business"] == 'OPEN'


@pytest.mark.django_db
def test_lists_invoice(api_client):
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    business_user = UserFactory.create(user_type=User.BUSINESS)
    contract = ContractFactory.create(
        business__user=business_user, property_obj__user=customer_user
    )
    invoice = InvoiceFactory.create(
        business=contract.business,
        property_obj=contract.property_obj,
        eoi=contract.eoi,
        contract=contract
    )

    api_client.force_authenticate(customer_user)
    response = api_client.get(reverse(viewname="invoices:invoice-list"), follow=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["id"] == invoice.id


@pytest.mark.django_db
@pytest.mark.skip
def test_customer_invoice_paid(api_client):
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    business_user = UserFactory.create(user_type=User.BUSINESS)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        first_payment_amount=0
    )
    invoice = InvoiceFactory.create(
        business=contract.business,
        property_obj=contract.property_obj,
        eoi=contract.eoi,
        contract=contract,
        status=1
    )

    api_client.force_authenticate(customer_user)
    response = api_client.post(reverse(viewname="invoices:invoice-paid", kwargs={"pk": invoice.id}), secure=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "PAID"
    assert response.data["status_business"] == "OPEN"


@pytest.mark.django_db
@pytest.mark.skip
def test_customer_invoice_paid_with_first_payment(api_client):
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    business_user = UserFactory.create(user_type=User.BUSINESS)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        first_payment_amount=20
    )
    invoice = InvoiceFactory.create(
        business=contract.business,
        property_obj=contract.property_obj,
        eoi=contract.eoi,
        contract=contract,
        status=1,
    )

    api_client.force_authenticate(customer_user)
    response = api_client.post(reverse(viewname="invoices:invoice-paid", kwargs={"pk": invoice.id}), secure=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "PENDING"
    assert response.data["status_business"] == "OPEN"


@pytest.mark.django_db
@pytest.mark.skip
def test_business_invoice_paid(api_client):
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    business_user = UserFactory.create(user_type=User.BUSINESS)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        first_payment_amount=0
    )
    invoice = InvoiceFactory.create(
        business=contract.business,
        property_obj=contract.property_obj,
        eoi=contract.eoi,
        contract=contract,
        status=1
    )

    api_client.force_authenticate(business_user)
    response = api_client.post(reverse(viewname="invoices:invoice-paid-business", kwargs={"pk": invoice.id}), secure=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "PAID"
    assert response.data["status"] == "OPEN"


@pytest.mark.django_db
@pytest.mark.skip
def test_business_invoice_paid_with_first_payment(api_client):
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    business_user = UserFactory.create(user_type=User.BUSINESS)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        first_payment_amount=20,
        status=Contract.IN_PROGRESS
    )
    invoice = Invoice.objects.filter(contract=contract).get()

    api_client.force_authenticate(business_user)
    # first payment marked as paid
    response = api_client.post(reverse(viewname="invoices:invoice-paid-business", kwargs={"pk": invoice.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "PENDING"
    assert response.data["status"] == "OPEN"

    # contract completed and invoice opened again
    response = api_client.post(reverse(viewname="contracts:contract-complete", kwargs={"pk": contract.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert invoice.status == Invoice.OPEN
    assert  invoice.status_business == Invoice.OPEN

    # last payment marked as paid
    response = api_client.post(reverse(viewname="invoices:invoice-paid-business", kwargs={"pk": invoice.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "PAID"
    assert response.data["status"] == "OPEN"


@pytest.mark.django_db
@pytest.mark.skip
def test_customer_invoice_paid_with_first_payment_after_business(api_client):
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    business_user = UserFactory.create(user_type=User.BUSINESS)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        first_payment_amount=20,
        status=Contract.IN_PROGRESS
    )
    invoice = Invoice.objects.filter(contract=contract).get()

    api_client.force_authenticate(business_user)
    # first payment marked as paid
    response = api_client.post(reverse(viewname="invoices:invoice-paid-business", kwargs={"pk": invoice.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "PENDING"
    assert response.data["status"] == "OPEN"

    api_client.force_authenticate(customer_user)
    response = api_client.post(reverse(viewname="invoices:invoice-paid", kwargs={"pk": invoice.id}),
                               secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "PENDING"
    assert response.data["status"] == "PENDING"

    api_client.force_authenticate(business_user)
    # contract completed and invoice opened again
    response = api_client.post(reverse(viewname="contracts:contract-complete", kwargs={"pk": contract.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert invoice.status == Invoice.OPEN
    assert  invoice.status_business == Invoice.OPEN

    # last payment marked as paid
    response = api_client.post(reverse(viewname="invoices:invoice-paid-business", kwargs={"pk": invoice.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "PAID"
    assert response.data["status"] == "OPEN"

    api_client.force_authenticate(customer_user)
    response = api_client.post(reverse(viewname="invoices:invoice-paid", kwargs={"pk": invoice.id}),
                               secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "PAID"
    assert response.data["status"] == "PAID"


@pytest.mark.django_db
@pytest.mark.skip
def test_business_invoice_paid_with_first_payment_after_customer(api_client):
    customer_user = UserFactory.create(user_type=User.CUSTOMER)
    business_user = UserFactory.create(user_type=User.BUSINESS)
    contract = ContractFactory.create(
        business__user=business_user,
        property_obj__user=customer_user,
        first_payment_amount=20,
        status=Contract.IN_PROGRESS
    )
    invoice = Invoice.objects.filter(contract=contract).get()

    api_client.force_authenticate(customer_user)
    # first payment marked as paid
    response = api_client.post(reverse(viewname="invoices:invoice-paid", kwargs={"pk": invoice.id}), secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "OPEN"
    assert response.data["status"] == "PENDING"

    api_client.force_authenticate(business_user)
    response = api_client.post(reverse(viewname="invoices:invoice-paid-business", kwargs={"pk": invoice.id}),
                               secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "PENDING"
    assert response.data["status"] == "PENDING"

    # contract completed by customer
    api_client.force_authenticate(customer_user)
    response = api_client.post(reverse(viewname="contracts:contract-complete", kwargs={"pk": contract.id}), secure=True)
    invoice = Invoice.objects.filter(contract=contract).get()
    assert response.status_code == status.HTTP_200_OK
    assert invoice.status == Invoice.PENDING
    assert invoice.status_business == Invoice.PENDING

    # contract completed by business and invoice opened again
    api_client.force_authenticate(business_user)
    response = api_client.post(reverse(viewname="contracts:contract-complete", kwargs={"pk": contract.id}), secure=True)
    invoice = Invoice.objects.filter(contract=contract).get()
    assert response.status_code == status.HTTP_200_OK
    assert invoice.status == Invoice.OPEN
    assert invoice.status_business == Invoice.OPEN

    api_client.force_authenticate(customer_user)
    # last payment marked as paid
    response = api_client.post(reverse(viewname="invoices:invoice-paid", kwargs={"pk": invoice.id}), secure=True)
    print("Response: ", response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "OPEN"
    assert response.data["status"] == "PAID"

    api_client.force_authenticate(business_user)
    response = api_client.post(reverse(viewname="invoices:invoice-paid-business", kwargs={"pk": invoice.id}),
                               secure=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status_business"] == "PAID"
    assert response.data["status"] == "PAID"
