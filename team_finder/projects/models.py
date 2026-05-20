from django.conf import settings
from django.db import models
from django.urls import reverse

TITLE_MAX_LENGTH = 200
STATUS_MAX_LENGTH = 20
SHORT_DESCRIPTION_MAX_LENGTH = 160
SHORT_DESCRIPTION_TRUNCATE_AT = 157


class Project(models.Model):
    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_FINISHED = 'finished'
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Открыт'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_FINISHED, 'Завершён'),
    )

    title = models.CharField('название', max_length=TITLE_MAX_LENGTH)
    description = models.TextField('описание', blank=True)
    status = models.CharField(
        'статус',
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='автор',
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='joined_projects',
        verbose_name='участники',
        blank=True,
    )
    skills = models.ManyToManyField(
        'skills.Skill',
        related_name='projects',
        verbose_name='навыки',
        blank=True,
    )
    created_at = models.DateTimeField('создан', auto_now_add=True)
    updated_at = models.DateTimeField('обновлён', auto_now=True)

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.pk})

    @property
    def short_description(self):
        if len(self.description) <= SHORT_DESCRIPTION_MAX_LENGTH:
            return self.description
        return self.description[:SHORT_DESCRIPTION_TRUNCATE_AT].rstrip() + '…'

    def is_finished(self):
        return self.status == self.STATUS_FINISHED
