
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include  # <-- MODIFIED: Added 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')), # <-- ADDED: Links your portal app
]