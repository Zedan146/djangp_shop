from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from . import models


class LoginForm(AuthenticationForm):
    """Аутентификация пользователя"""
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                 'placeholder': 'Пароль'}))


class RegistrationForm(UserCreationForm):
    """Регистрация пользователя"""

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Почта'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                  'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                            'placeholder': 'Повторите пароль'}))

    class Meta:
        model = models.User
        fields = ('username', 'email')
