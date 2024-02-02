from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from blog_api.utils.cookies import delete_access_and_refresh_cookie, set_access_cookie, set_refresh_cookie
from blog_api.utils.jwt import get_long_expiry_tokens_for_user, get_tokens_for_user, get_user_from_refresh_token

from .models import Token
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    ResetPasswordDoneSerializer,
    ResetPasswordSerializer,
    UserActivationSerializer,
    UserSerializer,
)

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"status": "success"}, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        remember_me = request.data.get("remember_me", None)
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get("refresh", None)
        access_token = response.data.get("access", None)
        access_expires = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        refresh_expires = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]

        if refresh_token and access_token:
            response.data = {}
            user = get_user_from_refresh_token(refresh_token)
            response.data["user"] = UserSerializer(user).data

            if remember_me:
                tokens = get_long_expiry_tokens_for_user(user)
                access_token = tokens.get("access_token")
                access_expires = tokens.get("access_expiry")
                refresh_token = tokens.get("refresh_token")
                refresh_expires = tokens.get("refresh_expiry")

            set_access_cookie(response, access_token, access_expires)
            set_refresh_cookie(response, refresh_token, refresh_expires)

        return response


@api_view(["POST"])
@permission_classes([AllowAny])
def activate(request):
    serializer = UserActivationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        # get token and mark as used
        token = Token.objects.get(token=serializer.data["token"])
        token.is_used = True
        token.save()
        # get user and set as active and set date verified
        user = token.user
        user.is_active = True
        user.verified_at = timezone.now()
        user.save()
        # set response
        response = Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        # set cookies
        tokens = get_tokens_for_user(user)
        set_access_cookie(response, tokens.get("access_token"))
        set_refresh_cookie(response, tokens.get("refresh_token"))

        return response

    except (Token.DoesNotExist, User.DoesNotExist):
        return Response({"status": "failed."}, status=status.HTTP_400_BAD_REQUEST)


class RefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        request.data["refresh"] = request.COOKIES.get("refresh_token")
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get("access", None)

        if access_token:
            response.data = {}
            set_access_cookie(response, access_token)

        return response


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"status": "success"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_done(request):
    serializer = ResetPasswordDoneSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"status": "success"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout_view(request):
    response = Response({"detail": "logout successful."}, status=status.HTTP_200_OK)
    return delete_access_and_refresh_cookie(response)


class UserViewSet(ModelViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
