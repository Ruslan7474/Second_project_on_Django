from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from apps.valuta.views import valuta_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('', include('apps.news.urls')),
    path('about/', include('apps.about.urls')),
    path('contacts/', include('apps.contact.urls')),
    path('application/', include('application.urls')),
    path('valuta/', valuta_page, name="valuta"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)