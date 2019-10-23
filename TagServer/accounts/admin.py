from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from django.contrib import admin


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Technical info", {
            'fields': ('role',),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Technical info", {
            'fields': ('role',),
        }),
    )
    list_display = ('username', 'role', )


admin.site.register(CustomUser, CustomUserAdmin)

