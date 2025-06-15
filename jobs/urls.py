from django.urls import path
from .views import my_protected_view, JobListCreateView, JobDetailView

urlpatterns = [
    path('protected/', my_protected_view, name='protected'),
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobDetailView.as_view()),
]
