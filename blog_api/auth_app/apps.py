from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog_api.auth_app"

    def ready(self) -> None:
        import blog_api.auth_app.signals.handlers  # noqa
