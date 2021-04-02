
from django.urls import path
from django.conf.urls import include, url 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', include('publis.urls')),
        url(r'^admin/', admin.site.urls),
     path('accounts/', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
