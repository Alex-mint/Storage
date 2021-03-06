from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from main.models import CartProduct, Cart, Customer, Order, Item, Image, \
    PageMessage, Storage, PageInfo, Category


class ImageInline(admin.TabularInline):
    model = Image
    fields = ['order', 'image', 'get_preview']
    readonly_fields = ["get_preview"]

    def get_preview(self, place):
        return format_html(
            '<img src="{}" width="auto" height="200px" />', place.image.url
        )



class ItemAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'get_preview')
    list_display_links = ('id', 'title',)
    readonly_fields = ('get_preview',)
    save_on_top = True

    def get_preview(self, item):
        return format_html(
            '<img src="{}" width="auto" height="200px" />', item.image.url
        )
    get_preview.short_description = 'Imagen'


class PageMessageAdmin(TranslationAdmin):
    list_display = ('title',)
    list_display_links = ('title',)


class PageInfoAdmin(TranslationAdmin):
    list_display = ('title',)
    list_display_links = ('title',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


admin.site.register(Item, ItemAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(PageMessage, PageMessageAdmin)
admin.site.register(PageInfo, PageMessageAdmin)
admin.site.register(Storage)
admin.site.register(Category)
