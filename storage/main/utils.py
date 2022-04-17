from django.db import models
from django.contrib import messages
from main.models import PageMessage


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count']
    cart.save()


def send_message(mesage, request):
    text = PageMessage.objects.get(title=mesage)
    messages.add_message(request, messages.INFO, text.text)