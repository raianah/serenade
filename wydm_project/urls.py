from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', include('wydm_app.urls')),  # Routes '/invite/' to wydm.urls
]
