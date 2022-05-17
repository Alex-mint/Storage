from django.contrib import admin

from emails.models import EmailType, EmailSendingFact

admin.site.register(EmailType)
admin.site.register(EmailSendingFact)
