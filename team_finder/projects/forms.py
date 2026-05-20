from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'status')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Например: Поиск тимлида для pet-проекта',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 6,
                'placeholder': 'Расскажите, чем будете заниматься, кого ищете…',
            }),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'status': 'Статус',
        }
