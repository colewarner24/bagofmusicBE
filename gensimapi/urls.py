from django.urls import path
from .views import query_albums

urlpatterns = [
    path('query/', query_albums, name='query_albums'),
]