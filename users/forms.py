from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django_registration.forms import RegistrationFormUniqueEmail as BaseRegistrationForm

from users.models import CustomUser
from green_space.form_mixins import FormMixin


class RegistrationForm(FormMixin, BaseRegistrationForm):
    is_nursery_manager = forms.BooleanField(required=False)
    style_attrs = {
        'username': {
            'placeholder': 'Username',
            'class': 'form-control',
        },
        'email': {
            'placeholder': 'Email',
            'class': 'form-control',
        },
        'password1': {
            'placeholder': 'Password',
            'class': 'form-control',
        },
        'password2': {
            'placeholder': 'Password again',
            'class': 'form-control',
        },
    }

    class Meta(BaseRegistrationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1',
                  'password2', 'is_nursery_manager', ]


class LoginForm(FormMixin, AuthenticationForm):
    style_attrs = {
        'username': {
            'placeholder': 'Username',
            'class': 'form-control',
        },
        'password': {
            'placeholder': 'Password',
            'class': 'form-control',
        },
    }
