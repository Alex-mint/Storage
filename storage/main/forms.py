import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.utils.translation import gettext_lazy as _

from datetime import timedelta

# class AddBookingForm(forms.Form):
#     first_name = forms.CharField(label='', widget=forms.TextInput(
#         attrs={'class': 'form-field', 'placeholder': _('Nombre')}))
#     last_name = forms.CharField(label='', widget=forms.TextInput(
#         attrs={'class': 'form-field', 'placeholder': _('Apellidos')}))
#     phone = forms.CharField(label='', widget=forms.TextInput(
#         attrs={'class': 'form-field', 'placeholder': _('Teléfono')}))
#     country = forms.ImageField(label='', widget=forms.TextInput(
#         attrs={'class': 'form-field', 'placeholder': _('Pais')}))
#     comment = forms.CharField(required=False, label='',
#                               widget=forms.Textarea(
#                                   attrs={'cols': 42, 'rows': 4,
#                                          'class': 'form-field',
#                                          'placeholder': _('Comentario')})
                              #)


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-field', 'placeholder': _('Usuario')}))
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'class': 'form-field', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-field', 'placeholder': _('Contraseña')}))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-field',
                                           'placeholder': _(
                                               'Rep. contraseña')}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-field', 'placeholder': _('Usuario')}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-field', 'placeholder': _('Contraseña')}))

