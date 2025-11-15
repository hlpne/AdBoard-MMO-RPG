"""
URL configuration for mmo_board project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Включает все URL для allauth, включая socialaccount
    path('accounts/', include('accounts.urls')),
    path('adverts/', include('adverts.urls')),
    path('replies/', include('replies.urls')),
    path('newsletters/', include('newsletters.urls')),
    path('', RedirectView.as_view(url='/adverts/', permanent=False), name='index'),
]

# В локальном окружении всегда отдаём медиа самим Django (без Nginx)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files from STATICFILES_DIRS
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

