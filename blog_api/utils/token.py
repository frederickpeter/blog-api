from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from blog_api.auth_app.models import Token

User = get_user_model()


class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Implement your custom hash value generation logic here
        # You can include any attributes or fields from the user object that you need for token generation
        return f"{user['id']}{timestamp}"


custom_token_generator = CustomTokenGenerator()


def generate_short_lived_verification_token(user):
    user_instance = User.objects.get(email=user["email"])
    default_token = custom_token_generator.make_token(user)
    expires_at = timezone.now() + timezone.timedelta(days=1)
    token = Token.objects.create(token=default_token, user=user_instance, expires_at=expires_at)
    return default_token if token else None


def generate_long_lived_verification_token(user):
    user_instance = User.objects.get(email=user["email"])
    default_token = custom_token_generator.make_token(user)
    expires_at = timezone.now() + timezone.timedelta(days=3)
    token = Token.objects.create(token=default_token, user=user_instance, expires_at=expires_at)
    return default_token if token else None


def check_token_expired_or_consumed(token, user):
    try:
        obj = Token.objects.get(token=token, user=user)
        return (obj and obj.is_used) or (obj and (timezone.now() > obj.expires_at))
    except Token.DoesNotExist:
        return True


def get_user_from_token_and_uid(uidb64, token: str):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None

    invalid = check_token_expired_or_consumed(token, user)
    return None if invalid else user


def get_user_from_token(token: str):
    try:
        token = Token.objects.get(token=token)
    except (TypeError, ValueError, OverflowError, Token.DoesNotExist):
        return None

    invalid = check_token_expired_or_consumed(token, token.user)
    return None if invalid else token.user
