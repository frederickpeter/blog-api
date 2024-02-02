import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from versatileimagefield.fields import VersatileImageField

from blog_api.utils.uploads import avatar_wrapper

from .managers import UserManager


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    avatar = VersatileImageField(upload_to=avatar_wrapper, null=True, blank=True)
    verified_at = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    # username field cannot be part of required fields
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]


class Token(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.token
