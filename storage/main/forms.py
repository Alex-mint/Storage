import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.utils.translation import gettext_lazy as _

from datetime import timedelta


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'email', 'city', 'street',
            'number', 'order_date', 'comment'
        )


class AddImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']


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
