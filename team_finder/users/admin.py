from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('-date_joined',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'username')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личные данные', {
            'fields': (
                'username', 'first_name', 'last_name', 'avatar',
                'bio', 'phone', 'github',
            ),
        }),
        ('Права доступа', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
            ),
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name',
                'password1', 'password2',
            ),
        }),
    )
