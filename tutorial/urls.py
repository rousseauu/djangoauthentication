from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from tutorial import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', include('home.urls', namespace='home')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)