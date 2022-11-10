from typing import List, Any

from django.core.mail import EmailMultiAlternatives

from danube import settings
from django.template import Template
from django.template.loader import get_template


def render_html(context, template_name):
    """Render html using template."""
    context["SITE_URL"] = settings.SITE_URL
    context["FRONTEND_URL"] = settings.FRONTEND_URL
    template: Template = get_template(template_name)
    body: str = template.render(context=context)
    return body


def send_email(
    emails: List[str],
    body: str,
    subject: str = "Billntrade team",
    attachments: Any = None,
    attachment_names: Any = None,
) -> None:
    """Send email to."""

    # body = "welcome"
    # emails = ["tomasbillion555@gmail.com"]
    # subject = "test"

    mail: EmailMultiAlternatives = EmailMultiAlternatives(
        subject=subject, body=body, from_email="support@billntrade.com",  to=emails
    )

    mail.attach_alternative(body, "text/html")
    if attachments:
        for file, name in zip(attachments, attachment_names):
            mail.attach(name, content=file)
    mail.send(fail_silently=False)
