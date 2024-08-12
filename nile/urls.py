from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fees.urls')),
    path('profile/', include('user.urls')),
    path('accounts/', include('allauth.urls')),
    # path('chaining/', include('smart_selects.urls')),
    re_path(r'^chaining/', include('smart_selects.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
