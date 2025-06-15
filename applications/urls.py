from django.urls import path
from .views import ApplicationListCreateView, ApplicationDetailView, MyApplicationsView, ResumeDownloadView, RecruiterJobApplicationsView

urlpatterns = [
    path('', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('<int:pk>/', ApplicationDetailView.as_view()),
    path('<int:pk>/resume/', ResumeDownloadView.as_view()),
    path('mine/', MyApplicationsView.as_view(), name="applicant-dashboard"),
    path('recruiter/applications/', RecruiterJobApplicationsView.as_view(), name="recruiter-dashboard"),
]
