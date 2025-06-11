from django.urls import path
from .views import my_protected_view

urlpatterns = [
    path('protected/', my_protected_view, name='protected'),
]
