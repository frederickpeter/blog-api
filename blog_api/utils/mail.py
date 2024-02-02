from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string

if settings.DEBUG:
    FRONTEND = "http://localhost:5173"
else:
    FRONTEND = "https://frontend.com"


def send_html_mail(template, subject, recipient, context):
    if not ("test" in recipient[0] or "mailinator" in recipient[0]):
        html_message = render_to_string(template, context=context)
        email_from = settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject=subject,
            message=html_message,
            from_email=email_from,
            recipient_list=recipient,
            html_message=html_message,
            fail_silently=False,
        )


def send_mass_html_mail(template, subject, recipients, context):
    html_message = render_to_string(template, context=context)
    email_from = settings.DEFAULT_FROM_EMAIL
    email_messages = [
        (subject, html_message, email_from, [recipient])
        for recipient in recipients
        if not ("test" in recipient[0] or "mailinator" in recipient[0])
    ]
    send_mass_mail(email_messages, fail_silently=False)


def send_plain_mail(subject, body, recipient):
    if not ("test" in recipient[0] or "mailinator" in recipient[0]):
        email_from = settings.DEFAULT_FROM_EMAIL
        send_mail(subject=subject, message=body, from_email=email_from, recipient_list=recipient, fail_silently=False)
