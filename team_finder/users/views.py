from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import EmailAuthenticationForm, ProfileEditForm, RegisterForm

User = get_user_model()


def _paginate(queryset, per_page, page_number):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('projects:project_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно. Войдите в систему.')
            return redirect('users:login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class EmailLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


def user_list(request):
    users_qs = User.objects.filter(is_active=True).order_by('-date_joined')
    page_obj = _paginate(users_qs, settings.USERS_PER_PAGE, request.GET.get('page'))
    return render(request, 'users/user_list.html', {'page_obj': page_obj})


def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    projects = user.projects.all().order_by('-created_at')
    return render(request, 'users/user_detail.html', {
        'profile_user': user,
        'projects': projects,
    })


@login_required
def user_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён.')
            return redirect('users:user_detail', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/user_edit.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
        return form


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'
