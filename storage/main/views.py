from django.shortcuts import render
from django.views.generic import ListView

from .models import Item


class Home(ListView):
    model = Item
    template_name = 'main/index.html'
    context_object_name = 'products'

