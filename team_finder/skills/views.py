from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from projects.models import Project

from .models import Skill

AUTOCOMPLETE_LIMIT = 8
SKILL_NAME_MAX_LENGTH = 64


@require_GET
def skill_autocomplete(request):
    query = (request.GET.get('q') or '').strip()
    if not query:
        return JsonResponse({'results': []})
    qs = Skill.objects.filter(name__icontains=query).order_by('name')[:AUTOCOMPLETE_LIMIT]
    results = [{'id': s.id, 'name': s.name, 'slug': s.slug} for s in qs]
    return JsonResponse({'results': results})


def _is_project_owner(user, project):
    return user.is_authenticated and project.author_id == user.id


@require_POST
@login_required
def project_skill_add(request, project_id):
    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse({'error': 'not_found'}, status=HTTPStatus.NOT_FOUND)

    if not _is_project_owner(request.user, project):
        return JsonResponse({'error': 'forbidden'}, status=HTTPStatus.FORBIDDEN)

    name = (request.POST.get('name') or '').strip()
    if not name:
        return JsonResponse({'error': 'empty'}, status=HTTPStatus.BAD_REQUEST)
    if len(name) > SKILL_NAME_MAX_LENGTH:
        return JsonResponse({'error': 'too_long'}, status=HTTPStatus.BAD_REQUEST)

    skill = Skill.objects.filter(name__iexact=name).first()
    if skill is None:
        skill = Skill.objects.create(name=name)

    project.skills.add(skill)
    return JsonResponse({
        'id': skill.id,
        'name': skill.name,
        'slug': skill.slug,
    })


@require_POST
@login_required
def project_skill_remove(request, project_id, skill_id):
    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse({'error': 'not_found'}, status=HTTPStatus.NOT_FOUND)

    if not _is_project_owner(request.user, project):
        return JsonResponse({'error': 'forbidden'}, status=HTTPStatus.FORBIDDEN)

    skill = Skill.objects.filter(pk=skill_id).first()
    if skill is None:
        return JsonResponse({'error': 'not_found'}, status=HTTPStatus.NOT_FOUND)

    project.skills.remove(skill)
    return JsonResponse({'ok': True, 'id': skill_id})
