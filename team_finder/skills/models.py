from django.db import models
from django.utils.text import slugify

SKILL_NAME_MAX_LENGTH = 64
SKILL_SLUG_MAX_LENGTH = 80


class Skill(models.Model):
    name = models.CharField('название', max_length=SKILL_NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField('слаг', max_length=SKILL_SLUG_MAX_LENGTH, unique=True, blank=True)

    class Meta:
        verbose_name = 'навык'
        verbose_name_plural = 'навыки'
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=False) or 'skill'
            candidate = base
            i = 1
            while Skill.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                i += 1
                candidate = f'{base}-{i}'
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
