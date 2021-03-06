from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from main import views

#from main.views import stripe_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    #path('', include('main.urls')),
]

urlpatterns += i18n_patterns(path('', include('main.urls')),)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

