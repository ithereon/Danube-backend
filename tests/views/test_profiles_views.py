# import pytest
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
#
# from danube.accounts.models import User
# from danube.profiles.models import BusinessDetails
# from tests.factories import (
#     ProfileFactory,
#     UserFactory,
#     PropertyFactory,
#     BusinessDetailsFactory,
# )
#
#
# @pytest.mark.django_db
# def test_create_profile(client_customer, customer):
#     profile_data = {
#         "title": "Miss",
#         "first_name": "An",
#         "last_name": "Test",
#         "user": customer.id,
#     }
#     response = client_customer.post(
#         reverse(viewname="profiles:profile-list"), data=profile_data
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data["first_name"] == "An"
#
#
# @pytest.mark.django_db
# def test_update_profile():
#     customer = UserFactory.create(user_type=User.CUSTOMER)
#     profile = ProfileFactory.create(user=customer)
#     new_first_name = "TestName"
#     profile_data = {
#         "first_name": new_first_name,
#     }
#     client = APIClient()
#     client.force_authenticate(user=customer)
#     response = client.patch(
#         reverse(viewname="profiles:profile-detail", kwargs={"pk": profile.id},),
#         data=profile_data,
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["first_name"] == new_first_name
#
#
# @pytest.mark.django_db
# def test_get_profiles_list_empty(client_business):
#     ProfileFactory.create_batch(10)
#     response = client_business.get(reverse(viewname="profiles:profile-list"))
#     assert response.status_code == status.HTTP_200_OK
#     assert not response.data["count"]
#
#
# @pytest.mark.django_db
# def test_get_profiles_list_only_you(client_business, business):
#     ProfileFactory.create_batch(10)
#     you = ProfileFactory.create(user=business)
#     response = client_business.get(reverse(viewname="profiles:profile-list"))
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data["results"]) == 1
#     assert response.data["results"][0]["last_name"] == you.last_name
#
#
# @pytest.mark.django_db
# def test_get_titles(client_business, business):
#     response = client_business.get(reverse(viewname="profiles:title"))
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data) == 9
#     assert response.data[0] == "Mr"
#
#
# @pytest.mark.django_db
# def test_create_property(property_dict):
#     user = UserFactory.create(user_type=1)
#     property_dict["user"] = user.id
#     client = APIClient()
#     client.force_authenticate(user=user)
#     response = client.post(
#         reverse(viewname="profiles:property-list"), data=property_dict
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data["address_1"] == property_dict["address_1"]
#
#
# @pytest.mark.django_db
# def test_update_property():
#     property = PropertyFactory.create()
#     new_county = "Test county"
#     client = APIClient()
#     client.force_authenticate(user=property.user)
#     response = client.patch(
#         reverse(viewname="profiles:property-detail", kwargs={"pk": property.id}),
#         data={"county": new_county},
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["county"] == new_county
#
#
# @pytest.mark.django_db
# def test_get_properties_list():
#     user = UserFactory.create()
#     PropertyFactory.create_batch(5)
#     PropertyFactory.create_batch(3, user=user)
#     client = APIClient()
#     client.force_authenticate(user=user)
#     response = client.get(reverse(viewname="profiles:property-list"))
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["count"] == 3
#     assert response.data["results"][0]["user"] == user.id
#
#
# @pytest.mark.django_db
# def test_get_properties_detail():
#     user = UserFactory.create()
#     property = PropertyFactory.create(user=user)
#     client = APIClient()
#     client.force_authenticate(user=user)
#     response = client.get(
#         reverse(viewname="profiles:property-detail", kwargs={"pk": property.id})
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["id"] == property.id
#
#
# @pytest.mark.django_db
# def test_create_business_details(business_details_dict):
#     user = UserFactory.create(user_type=1)
#     business_details_dict["user"] = user.id
#     client = APIClient()
#     client.force_authenticate(user=user)
#     response = client.post(
#         reverse(viewname="profiles:business_details-list"), data=business_details_dict
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.data["description"] == business_details_dict["description"]
#
#
# @pytest.mark.django_db
# def test_update_business_details():
#     details = BusinessDetailsFactory.create()
#     new_name = "The best company name"
#     client = APIClient()
#     client.force_authenticate(user=details.user)
#     response = client.patch(
#         reverse(viewname="profiles:business_details-detail", kwargs={"pk": details.id}),
#         data={"business_name": new_name},
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["business_name"] == new_name
#
#
# @pytest.mark.django_db
# def test_get_business_details_list():
#     BusinessDetailsFactory.create_batch(10)
#     you = BusinessDetailsFactory.create()
#     client = APIClient()
#     client.force_authenticate(user=you.user)
#     response = client.get(reverse(viewname="profiles:business_details-list"))
#     business_details_count = BusinessDetails.objects.count()
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["count"] == business_details_count
#
#
# @pytest.mark.django_db
# def test_get_business_details_detail():
#     user = UserFactory.create()
#     details = BusinessDetailsFactory.create(user=user)
#     client = APIClient()
#     client.force_authenticate(user=user)
#     response = client.get(
#         reverse(viewname="profiles:business_details-detail", kwargs={"pk": details.id})
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["id"] == details.id
#     assert response.data["postcode"] == details.postcode
