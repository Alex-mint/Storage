import folium
from django.db import models
from django.contrib import messages
from main.models import PageMessage


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum'] * cart.month
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count']
    cart.save()


def send_message(mesage, request):
    text = PageMessage.objects.get(title=mesage)
    messages.add_message(request, messages.INFO, text.text)


def get_map(storage):
    TABLERO = [27.767199, -15.609078]
    map = folium.Map(location=TABLERO, zoom_start=17)
    folium.Marker(
        location=[storage.lat, storage.lon],
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(map)
    return map