from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404

urlpatterns = [
    path('', include("home.urls")),
    path('admin/', admin.site.urls),
    path('profile/', include("profiles.urls")),
    path('hoctap/', include('hoctap_main.urls')),
    path('hoctap-others/', include('hoctap_others.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
