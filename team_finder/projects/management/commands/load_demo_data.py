"""Seed the database with demo users, skills, and projects.

Idempotent: if any non-superuser already exists, the command exits.
Called from entrypoint.sh on container start.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from projects.models import Project
from skills.models import Skill

User = get_user_model()


DEMO_USERS = [
    {
        'email': 'anna@example.com',
        'first_name': 'Анна', 'last_name': 'Смирнова',
        'password': 'TeamFinder123!',
        'bio': 'Frontend-разработчик. Люблю React и красивый UI.',
        'phone': '+7 916 100-10-10', 'github': 'anna-smirnova',
    },
    {
        'email': 'boris@example.com',
        'first_name': 'Борис', 'last_name': 'Петров',
        'password': 'TeamFinder123!',
        'bio': 'Backend на Django, 4 года опыта. Ищу команду для pet-проектов.',
        'phone': '+7 916 200-20-20', 'github': 'boris-p',
    },
    {
        'email': 'victoria@example.com',
        'first_name': 'Виктория', 'last_name': 'Кузнецова',
        'password': 'TeamFinder123!',
        'bio': 'ML-инженер, NLP, RecSys. Открыта к опенсорс-проектам.',
        'phone': '+7 916 300-30-30', 'github': 'vic-kuz',
    },
    {
        'email': 'denis@example.com',
        'first_name': 'Денис', 'last_name': 'Орлов',
        'password': 'TeamFinder123!',
        'bio': 'DevOps. Kubernetes, CI/CD, мониторинг.',
        'phone': '+7 916 400-40-40', 'github': 'denis-orlov',
    },
    {
        'email': 'elena@example.com',
        'first_name': 'Елена', 'last_name': 'Соколова',
        'password': 'TeamFinder123!',
        'bio': 'UX/UI-дизайнер. Делаю интерфейсы, которые понятны без подсказок.',
        'phone': '+7 916 500-50-50', 'github': 'elena-sk',
    },
]

DEMO_SKILLS = [
    'Python', 'Django', 'PostgreSQL', 'Docker', 'React', 'TypeScript',
    'JavaScript', 'CSS', 'HTML', 'FastAPI', 'Machine Learning', 'NLP',
    'Kubernetes', 'CI/CD', 'Figma', 'UX-дизайн', 'Go', 'Rust',
]

DEMO_PROJECTS = [
    {
        'title': 'Платформа для онлайн-курсов по программированию',
        'author_email': 'anna@example.com',
        'status': Project.STATUS_OPEN,
        'description': (
            'Делаем платформу, где разработчики смогут проходить интерактивные '
            'курсы прямо в браузере. Ищу backend-разработчика и дизайнера.'
        ),
        'skills': ['Python', 'Django', 'PostgreSQL', 'React'],
    },
    {
        'title': 'Telegram-бот для трекинга финансов',
        'author_email': 'boris@example.com',
        'status': Project.STATUS_IN_PROGRESS,
        'description': (
            'MVP уже готов. Нужна помощь с интеграцией бирж и улучшением UX. '
            'Ищу человека с опытом в FastAPI и немного фронтенда.'
        ),
        'skills': ['Python', 'FastAPI', 'PostgreSQL'],
    },
    {
        'title': 'Рекомендательная система для подкастов',
        'author_email': 'victoria@example.com',
        'status': Project.STATUS_OPEN,
        'description': (
            'Pet-проект: рекомендую подкасты на основе истории прослушивания. '
            'Нужна команда: ML-инженер ещё, backend, фронт.'
        ),
        'skills': ['Python', 'Machine Learning', 'NLP', 'PostgreSQL'],
    },
    {
        'title': 'Self-hosted dashboard для домашнего сервера',
        'author_email': 'denis@example.com',
        'status': Project.STATUS_OPEN,
        'description': (
            'Open-source проект — единая панель для управления домашним '
            'кластером. Frontend на React, backend на Go.'
        ),
        'skills': ['Go', 'React', 'TypeScript', 'Docker', 'Kubernetes'],
    },
    {
        'title': 'Маркетплейс фриланс-дизайнеров',
        'author_email': 'elena@example.com',
        'status': Project.STATUS_OPEN,
        'description': (
            'Платформа, где заказчики могут найти дизайнера по портфолио, '
            'а не по тарифу. Нужны разработчики и продакт.'
        ),
        'skills': ['Figma', 'UX-дизайн', 'React', 'Django', 'PostgreSQL'],
    },
    {
        'title': 'Игровой движок 2D для образовательных целей',
        'author_email': 'boris@example.com',
        'status': Project.STATUS_OPEN,
        'description': (
            'Минималистичный движок, на котором школьники смогут делать '
            'свои первые игры. Rust + WebAssembly.'
        ),
        'skills': ['Rust', 'JavaScript', 'CSS', 'HTML'],
    },
    {
        'title': 'Сборник материалов для подготовки к собеседованиям',
        'author_email': 'anna@example.com',
        'status': Project.STATUS_FINISHED,
        'description': (
            'Open-source репозиторий со структурированными материалами. '
            'Сейчас стабильно поддерживается сообществом.'
        ),
        'skills': ['JavaScript', 'CSS', 'HTML'],
    },
    {
        'title': 'Сервис заметок с end-to-end шифрованием',
        'author_email': 'victoria@example.com',
        'status': Project.STATUS_OPEN,
        'description': (
            'Заметки, доступ к которым невозможен без ключа клиента. '
            'Нужен криптоэнтузиаст и хороший фронтенд-разработчик.'
        ),
        'skills': ['TypeScript', 'React', 'Python', 'FastAPI'],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with demo users, skills, and projects.'

    @transaction.atomic
    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=False).exists():
            self.stdout.write(self.style.WARNING(
                'Demo data already loaded — skipping.'
            ))
            return

        # Superuser
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin12345',
                first_name='Админ',
                last_name='Админов',
            )
            self.stdout.write(self.style.SUCCESS(
                'Created superuser admin@example.com / admin12345'
            ))

        # Users
        users = {}
        for data in DEMO_USERS:
            user = User.objects.create_user(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                bio=data['bio'],
                phone=data['phone'],
                github=data['github'],
            )
            users[data['email']] = user
            self.stdout.write(f'  + user {user.email}')

        # Skills
        skills = {}
        for name in DEMO_SKILLS:
            skill, _ = Skill.objects.get_or_create(name=name)
            skills[name] = skill
        self.stdout.write(f'  + {len(skills)} skills')

        # Projects
        for data in DEMO_PROJECTS:
            project = Project.objects.create(
                title=data['title'],
                description=data['description'],
                status=data['status'],
                author=users[data['author_email']],
            )
            project.skills.set([skills[n] for n in data['skills']])
            self.stdout.write(f'  + project «{project.title}»')

        self.stdout.write(self.style.SUCCESS('Demo data loaded.'))
