import copy

from django.urls import reverse
from django_rest_passwordreset.models import ResetPasswordToken

from .test_setup import TestSetUp
from ..models import User


class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["email"], self.user_data["email"])
        self.assertEqual(res.data["username"], self.user_data["username"])

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 401)

    def test_user_can_login_after_verification(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 201)
        email = response.data["email"]
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)

    def test_user_reset_password(self):
        # Create user
        user_data = copy.deepcopy(self.user_data)
        user_data["email"] = self.fake.email()
        user_data["username"] = self.fake.email().split("@")[0]
        user_data.pop("password2")
        user = User.objects.create_user(**user_data)
        user.is_active = True
        user.save()
        # Generate reset token
        token = ResetPasswordToken.objects.create(user=user,)
        # Set a new password
        url = reverse("password_reset:reset-password-confirm")
        new_password = "test12345678"
        res = self.client.post(
            url, {"token": token.key, "password": new_password}, format="json"
        )
        self.assertEqual(res.status_code, 200)
        # Login with a new password
        res = self.client.post(
            self.login_url,
            {"email": user_data["email"], "password": new_password},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
