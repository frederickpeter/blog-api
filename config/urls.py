from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_nested import routers

from blog_api.auth_app.urls import router as auth_router
from blog_api.auth_app.views import (
    LoginView,
    RefreshView,
    activate,
    logout_view,
    register,
    reset_password,
    reset_password_done,
)

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.registry.extend(auth_router.registry)

urlpatterns = [
    path("accounts/register/", register, name="register"),
    path("accounts/activate/", activate, name="activate"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", logout_view, name="logout"),
    path("accounts/reset/password/", reset_password, name="reset_password"),
    path("accounts/reset/password/done/", reset_password_done, name="reset_password_done"),
    path("accounts/refresh/", RefreshView.as_view(), name="refresh"),
    path("api/", include(router.urls)),
    #
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
