from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Application
from jobs.models import Job
from jobs.views import IsRecruiter
from .serializers import ApplicationSerializer
from django.http import FileResponse, Http404
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import os


class RecruiterJobApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self): # type: ignore
        return Application.objects.filter(job__posted_by=self.request.user)


class ResumeDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)

            # Only the applicant or staff can download
            if application.applicant != request.user and not request.user.is_staff:
                return Response({"detail": "Not authorized to view this resume."}, status=403)

            if not application.resume:
                return Response({"detail": "No resume uploaded."}, status=404)

            resume_path = os.path.join(settings.MEDIA_ROOT, application.resume.name)

            return FileResponse(open(resume_path, 'rb'), content_type='application/octet-stream')
        except Application.DoesNotExist:
            raise Http404("Application not found.")


class MyApplicationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        applications = Application.objects.filter(applicant=user)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class ApplicationListCreateView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        job_id = self.request.data.get('job')   # type: ignore
        job = get_object_or_404(Job, id=job_id)
        serializer.save(applicant=self.request.user, job=job)
        send_mail(
            subject=f"New application for {job.title}",
            message=f"{self.request.user.email} applied to your job.",  # type: ignore
            from_email=None,
            recipient_list=[job.posted_by.email],
        )



class ApplicationDetailView(generics.RetrieveDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
