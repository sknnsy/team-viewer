from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'author__email')
    autocomplete_fields = ('author',)
    filter_horizontal = ('skills', 'members')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
