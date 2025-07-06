from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "city",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "city",
    )
    search_fields = ("username", "email")
