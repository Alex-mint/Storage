from django.contrib import admin
from django.utils.html import format_html

from main.models import CartProduct, Cart, Customer, Order, Item, Image, PageMessage


class ImageInline(admin.TabularInline):
    model = Image
    fields = ['order', 'image', 'get_preview']
    readonly_fields = ["get_preview"]

    def get_preview(self, place):
        return format_html(
            '<img src="{}" width="auto" height="200px" />', place.image.url
        )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]

admin.site.register(Item)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(PageMessage)
