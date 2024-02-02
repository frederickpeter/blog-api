from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
    }


def get_long_expiry_tokens_for_user(user):
    access_token = AccessToken.for_user(user)
    access_token.set_exp(lifetime=timedelta(days=1))
    access_expires = timedelta(days=1)

    refresh_token = RefreshToken.for_user(user)
    refresh_token.set_exp(lifetime=timedelta(days=5))
    refresh_expires = timedelta(days=5)

    return {
        "access_token": access_token,
        "access_expiry": access_expires,
        "refresh_token": refresh_token,
        "refresh_expiry": refresh_expires,
    }


def get_user_from_refresh_token(refresh):
    refresh = RefreshToken(refresh)
    user_id = refresh["user_id"]
    user = User.objects.get(id=user_id)
    return user if user else None


def get_access_token_from_refresh_token(refresh):
    refresh = RefreshToken(refresh)
    return (str(refresh.access_token),)
