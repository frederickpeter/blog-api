from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from blog_api.utils.mail import FRONTEND, send_html_mail
from blog_api.utils.token import generate_long_lived_verification_token, generate_short_lived_verification_token


def user_registration_mail(user):
    token = generate_long_lived_verification_token(user)
    if token:
        context = {
            "frontend": FRONTEND,
            "uid": urlsafe_base64_encode(force_bytes(user["id"])),
            "token": token,
            "name": user["name"],
            "topic": f"You have successfully created an account using {user['email']}",
            "body": "Click on the following link to verify your account:",
        }
        send_html_mail("verify_email.html", f"Welcome {user['name']}", [user["email"]], context)


def password_updated_mail(user):
    context = {
        "name": user["name"],
        "email": user["email"],
        "topic": "You have successfully updated your password.",
    }
    send_html_mail("password_updated_email.html", "Password Updated", [user["email"]], context)


def reset_password_mail(user):
    token = generate_short_lived_verification_token(user)
    if token:
        context = {
            "frontend": FRONTEND,
            "uid": urlsafe_base64_encode(force_bytes(user["id"])),
            "token": token,
            "email": user["email"],
            "topic": f"You requested to reset your password using {user['email']}",
            "body": "Click on the following link to reset your password:",
        }
        send_html_mail("reset_password.html", "Password Reset", [user["email"]], context)
