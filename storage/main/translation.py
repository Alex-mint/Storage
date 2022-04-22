from modeltranslation.translator import register, TranslationOptions
from .models import Item, PageInfo, PageMessage
from emails.models import EmailType


@register(Item)
class ApartmentTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(PageInfo)
class PageInfoTranslationOptions(TranslationOptions):
    fields = ('title', 'info',)


@register(PageMessage)
class PageMessageTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(EmailType)
class EmailTypeTranslationOptions(TranslationOptions):
    fields = ('message_2', 'message_1', 'subject')
