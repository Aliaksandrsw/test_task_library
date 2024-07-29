from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('libra.urls')),
    path('users/', include('users.urls')),
    path('api/', include('library_api.urls')),
]
