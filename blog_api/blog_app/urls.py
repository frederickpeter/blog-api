from django.conf import settings
from rest_framework import routers
from .views import CategoryViewset, PostViewset

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

# http://127.0.0.1:8000/categories/
router.register("categories", CategoryViewset, basename="categories")
# http://127.0.0.1:8000/posts/
router.register("posts", PostViewset, basename="posts")