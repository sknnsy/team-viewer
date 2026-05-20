"""URL configuration for Team Finder project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='projects:project_list', permanent=False)),
    path('project/', include('projects.urls', namespace='projects')),
    path('user/', include('users.urls', namespace='users')),
    path('skill/', include('skills.urls', namespace='skills')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
