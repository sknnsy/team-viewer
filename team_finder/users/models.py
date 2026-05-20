from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager

USERNAME_MAX_LENGTH = 150
FIRST_NAME_MAX_LENGTH = 150
LAST_NAME_MAX_LENGTH = 150
PHONE_MAX_LENGTH = 32
GITHUB_MAX_LENGTH = 150


class User(AbstractUser):
    username = models.CharField(max_length=USERNAME_MAX_LENGTH, unique=True, blank=True)
    email = models.EmailField('email', unique=True)
    first_name = models.CharField('имя', max_length=FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField('фамилия', max_length=LAST_NAME_MAX_LENGTH)

    avatar = models.ImageField(
        'аватар', upload_to='avatars/', blank=True, null=True
    )
    bio = models.TextField('о себе', blank=True)

    phone = models.CharField('телефон', max_length=PHONE_MAX_LENGTH, blank=True)
    github = models.CharField('github', max_length=GITHUB_MAX_LENGTH, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    def save(self, *args, **kwargs):
        if not self.username:
            base = self.email.split('@')[0]
            candidate = base
            i = 1
            while User.objects.filter(username=candidate).exclude(pk=self.pk).exists():
                i += 1
                candidate = f'{base}{i}'
            self.username = candidate
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name() or self.email
