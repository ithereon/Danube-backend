from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import int_list_validator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from common.email_sender import render_html, send_email


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(email, password, **extra_fields)

MR = 1
MS = 2
MRS = 3
DR = 4
MISS = 5
THEM = 6
THEY = 7
HE = 8
SHE = 9

TITLES_CHOICE = (
    (MR, "Mr"),
    (MS, "Ms"),
    (MRS, "Mrs"),
    (DR, "Dr"),
    (MISS, "Miss"),
    (THEM, "Them"),
    (THEY, "They"),
    (HE, "He"),
    (SHE, "She"),
)
class User(AbstractBaseUser, PermissionsMixin):
    CUSTOMER = 1
    BUSINESS = 2
    EMPLOYEE = 3
    REGISTRATION_ROLE_CHOICES = (
        (CUSTOMER, "Customer"),
        (BUSINESS, "Business"),
    )
    ROLES_CHOICES = (
        *REGISTRATION_ROLE_CHOICES,
        (EMPLOYEE, "Employee"),
    )
    email = models.EmailField(_("email address"), unique=True)
    title = models.PositiveIntegerField(choices=TITLES_CHOICE, null=True, blank=True)
    mobile = models.CharField(
        max_length=11,
        validators=[int_list_validator(sep=""), MinLengthValidator(11), ],
        default="12345678901",
    )
    username = models.CharField(_("username"), max_length=300)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    user_type = models.PositiveIntegerField(choices=ROLES_CHOICES, default=CUSTOMER)

    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    is_active = models.BooleanField(_("active"), default=False)
    is_staff = models.BooleanField(_("staff"), default=False)
    is_superuser = models.BooleanField(_("superuser"), default=False)

    first_login = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def send_activation_email(self):
        token = RefreshToken.for_user(self).access_token
        context = {
            "token": token,
        }
        email = str(self.email)
        body = render_html(context=context, template_name="emails/signup.html")
        print(body)
        send_email(emails=[email], body=body)
        
    @property
    def is_customer(self):
        return self.user_type == self.CUSTOMER

    @property
    def is_employee(self):
        return self.user_type in (self.EMPLOYEE, self.BUSINESS)
