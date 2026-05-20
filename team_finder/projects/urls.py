from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/join/', views.project_join, name='project_join'),
    path('<int:pk>/finish/', views.project_finish, name='project_finish'),
]
