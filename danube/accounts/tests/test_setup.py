from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse("api-register")
        self.login_url = reverse("api-login")
        self.fake = Faker()
        password = "Test!!1."
        self.user_data = {
            "email": self.fake.email(),
            "usertype": "Customer",
            "username": self.fake.email().split("@")[0],
            "password": password,
            "password2": password,
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
