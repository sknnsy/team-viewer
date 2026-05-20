from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.EmailLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('list/', views.user_list, name='user_list'),
    path('edit/', views.user_edit, name='user_edit'),
    path(
        'password-change/',
        views.CustomPasswordChangeView.as_view(),
        name='password_change',
    ),
    path(
        'password-change/done/',
        views.CustomPasswordChangeDoneView.as_view(),
        name='password_change_done',
    ),
    path('<str:username>/', views.user_detail, name='user_detail'),
]
