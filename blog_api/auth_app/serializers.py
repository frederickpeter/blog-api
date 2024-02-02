from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer

from blog_api.auth_app.tasks import send_reset_password_mail, send_verify_account_html_mail
from blog_api.utils.token import get_user_from_token_and_uid

from .models import Token

User = get_user_model()


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
            if user.verified_at is None:
                send_verify_account_html_mail.delay({"id": str(user.id), "name": user.name, "email": user.email})
                raise serializers.ValidationError("Verification mail has been resent")
        except User.DoesNotExist:
            return super().validate(attrs)

        return super().validate(attrs)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data["password"]
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.is_active = False
        instance.last_login = None
        instance.save()

        # exclude avatar because image fields are not json serializable
        send_verify_account_html_mail.delay({"id": str(instance.id), "name": instance.name, "email": instance.email})
        return instance


class UserActivationSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=False)
    uid = serializers.CharField(allow_blank=False)

    def validate(self, data):
        user = get_user_from_token_and_uid(data["uid"], data["token"])
        if user is None:
            raise serializers.ValidationError("Error! Token is invalid")
        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Invalid Email")
        return value

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        send_reset_password_mail.delay({"id": str(user.id), "name": user.name, "email": user.email})


class ResetPasswordDoneSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=False)
    uid = serializers.CharField(allow_blank=False)
    password = serializers.CharField(max_length=255, allow_blank=False)
    confirm_password = serializers.CharField(max_length=255, allow_blank=False)

    def validate(self, data):
        user = get_user_from_token_and_uid(data["uid"], data["token"])
        if user is None:
            raise serializers.ValidationError("Error! Token is invalid")
        return data

    def validate_password(self, value):
        if value != self.initial_data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return value

    def save(self):
        try:
            # get token and mark as used
            user_token = self.validated_data["token"]
            token = Token.objects.get(token=user_token)
            token.is_used = True
            token.save()
            # get user and set as active
            user = token.user
            user.set_password(self.validated_data["password"])
            user.save()
        except (Token.DoesNotExist, User.DoesNotExist):
            raise serializers.ValidationError("Error! Token is invalid")


class UserSerializer(serializers.ModelSerializer):
    avatar = VersatileImageFieldSerializer(sizes="headshot")

    class Meta:
        model = User
        fields = ("id", "email", "name", "avatar", "last_login", "date_joined")
        read_only_fields = ["last_login", "date_joined"]
