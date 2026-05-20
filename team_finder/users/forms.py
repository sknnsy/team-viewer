from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()

FIRST_NAME_MAX_LENGTH = 150
LAST_NAME_MAX_LENGTH = 150


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        max_length=FIRST_NAME_MAX_LENGTH,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иван'}),
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=LAST_NAME_MAX_LENGTH,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Иванов'}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'you@example.com'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('password1', 'password2'):
            self.fields[name].widget.attrs.update({'class': 'form-input'})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'autofocus': True,
            'placeholder': 'you@example.com',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-input'})


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'bio', 'phone', 'github')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'phone': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': '+7 999 000-00-00',
            }),
            'github': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'github-username',
            }),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-file'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'avatar': 'Аватар',
            'bio': 'О себе',
            'phone': 'Телефон',
            'github': 'GitHub',
        }
