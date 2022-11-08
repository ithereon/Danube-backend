"""Request signals."""

import logging
from smtplib import SMTPException

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from danube.accounts.models import User
from common.email_sender import render_html, send_email

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_activation_emails(instance: User, **kwargs: dict) -> None:
    """Send emails to verify account."""
    if not instance.is_active and kwargs.get("created") is True:
        try:
            instance.send_activation_email()
        except SMTPException as e:
            logger.error(e)


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    context = {"token": reset_password_token.key}
    body = render_html(context=context, template_name="emails/reset_password.html")
    email = str(reset_password_token.user.email)
    send_email(emails=[email], body=body, subject="Password Reset")
