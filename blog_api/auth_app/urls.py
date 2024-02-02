from django.conf import settings
from rest_framework_nested import routers

from . import views

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

# http://127.0.0.1:8000/users/
router.register("users", views.UserViewSet)
