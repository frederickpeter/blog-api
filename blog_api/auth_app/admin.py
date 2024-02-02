from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from blog_api.auth_app.models import Token

User = get_user_model()
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "name", "email", "is_staff", "is_superuser", "is_active")
    readonly_fields = ["last_login", "date_joined"]
    list_per_page = 10
    search_fields = ["name"]
    actions = ["deactivate_user", "activate_user"]
    list_filter = ["is_staff", "is_superuser", "is_active"]

    # fieldsets is the form for editing or viewing an entity
    # the first index of each tuple is the name of the section: ex. 'Personal Information', 'Role Status'
    fieldsets = (
        (
            "Peronal Information",
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password"),
            },
        ),
        (
            "Role Status",
            {
                "classes": ("wide",),
                "fields": ("is_staff", "is_superuser", "is_active", "avatar"),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("wide",),
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "Date Information",
            {
                "classes": ("wide",),
                "fields": ("last_login", "date_joined", "verified_at"),
            },
        ),
    )

    # add_fieldsets is the form for adding/creating a new entity
    # the first index of each tuple is the name of the section: ex. 'Personal Information', 'Role Status'
    add_fieldsets = (
        (
            "Peronal Information",
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
        (
            "Role Status",
            {
                "classes": ("wide",),
                "fields": ("is_staff", "is_superuser", "is_active"),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("wide",),
                "fields": ("groups", "user_permissions"),
            },
        ),
    )

    # table should be ordered by name
    ordering = ("name",)
    # search by email, name
    search_fields = ("email", "name")

    # action to activate users
    @admin.action(description="Activate user(s)")
    def activate_user(self, request, queryset):
        updated_users = queryset.update(is_active=True)
        self.message_user(request, f"{updated_users} users were successfully activated.", messages.SUCCESS)

    # action to deactivate users
    @admin.action(description="Deactivate user(s)")
    def deactivate_user(self, request, queryset):
        updated_users = queryset.update(is_active=False)
        self.message_user(request, f"{updated_users} users were successfully deactivated.", messages.SUCCESS)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    list_display = ["id", "token", "user", "is_used"]
    list_per_page = 20
    list_filter = ["is_used"]
