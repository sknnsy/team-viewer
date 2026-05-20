from django.urls import path

from . import views

app_name = 'skills'

urlpatterns = [
    path('autocomplete/', views.skill_autocomplete, name='autocomplete'),
    path(
        'project/<int:project_id>/add/',
        views.project_skill_add,
        name='project_skill_add',
    ),
    path(
        'project/<int:project_id>/remove/<int:skill_id>/',
        views.project_skill_remove,
        name='project_skill_remove',
    ),
]
