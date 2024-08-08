from django.contrib import admin
from django.urls import path, include
from .views import csrf_token_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gensimapi.urls')),
    path('csrf-token/', csrf_token_view, name='csrf_token'),
]