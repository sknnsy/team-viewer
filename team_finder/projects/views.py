from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from skills.models import Skill

from .forms import ProjectForm
from .models import Project


def _paginate(queryset, per_page, page_number):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def project_list(request):
    projects_qs = (
        Project.objects.select_related('author')
        .prefetch_related('skills')
        .order_by('-created_at')
    )

    selected_skill = None
    skill_param = (request.GET.get('skill') or '').strip()
    if skill_param:
        selected_skill = (
            Skill.objects.filter(slug=skill_param).first()
            or Skill.objects.filter(name__iexact=skill_param).first()
        )
        if selected_skill is not None:
            projects_qs = projects_qs.filter(skills=selected_skill)
        else:
            projects_qs = projects_qs.none()

    all_skills = (
        Skill.objects.filter(projects__isnull=False)
        .distinct()
        .order_by('name')
    )

    page_obj = _paginate(projects_qs, settings.PROJECTS_PER_PAGE, request.GET.get('page'))

    return render(request, 'projects/project_list.html', {
        'page_obj': page_obj,
        'all_skills': all_skills,
        'selected_skill': selected_skill,
        'skill_param': skill_param,
    })


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.select_related('author').prefetch_related('skills', 'members'),
        pk=pk,
    )
    is_owner = request.user.is_authenticated and request.user.id == project.author_id
    is_member = (
        request.user.is_authenticated
        and project.members.filter(pk=request.user.pk).exists()
    )
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'is_owner': is_owner,
        'is_member': is_member,
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            form.save_m2m()
            messages.success(request, 'Проект опубликован.')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {
        'form': form,
        'is_edit': False,
    })


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.author_id != request.user.id:
        return HttpResponseForbidden('Нет прав на редактирование этого проекта.')
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены.')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {
        'form': form,
        'is_edit': True,
        'project': project,
    })


@login_required
def project_join(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method != 'POST':
        return redirect('projects:project_detail', pk=pk)
    if project.author_id == request.user.id:
        messages.info(request, 'Вы автор проекта.')
    elif project.is_finished():
        messages.warning(request, 'Проект завершён, к нему нельзя присоединиться.')
    elif project.members.filter(pk=request.user.pk).exists():
        messages.info(request, 'Вы уже участник проекта.')
    else:
        project.members.add(request.user)
        messages.success(request, 'Вы присоединились к проекту.')
    return redirect('projects:project_detail', pk=pk)


@login_required
def project_finish(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.author_id != request.user.id:
        return HttpResponseForbidden('Нет прав.')
    if request.method == 'POST':
        project.status = Project.STATUS_FINISHED
        project.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'Проект завершён.')
    return redirect('projects:project_detail', pk=pk)
