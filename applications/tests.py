from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from jobs.models import Job
from applications.models import Application

class ApplicationTests(APITestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(email="recruiter@example.com", password="pass", is_recruiter=True)    # type: ignore
        self.job = Job.objects.create(title="Test Job", description="...", posted_by=self.recruiter)
        self.user = User.objects.create_user(email="user@example.com", password="pass") # type: ignore

    def test_user_can_apply(self):
        self.client.force_authenticate(user=self.user)  # type: ignore
        url = reverse("application-list-create")
        with open("resume.txt", "w") as f:
            f.write("Test Resume")

        with open("resume.txt", "rb") as resume:
            data = {
                "job": self.job.id, # type: ignore
                "resume": resume,
                "cover_letter": "I'm great!"
            }
            response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)


class DashboardTests(APITestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(email="recruiter@example.com", password="pass123", is_recruiter=True) # type: ignore
        self.applicant = User.objects.create_user(email="applicant@example.com", password="pass123", is_recruiter=False)    # type: ignore
        self.recruiter_response = self.client.post("/api/token/", {"email": "recruiter@example.com", "password": "pass123"})
        self.applicant_response = self.client.post("/api/token/", {"email": "applicant@example.com", "password": "pass123"})
        self.recruiter_token = self.recruiter_response.data["access"]   # type: ignore
        self.applicant_token = self.applicant_response.data["access"]   # type: ignore



        self.job = Job.objects.create(
            title="Software Dev",
            description="Write code",
            company="Tech Corp",
            location="Nairobi",
            salary=150000.00,
            posted_by=self.recruiter
        )

        self.application = Application.objects.create(
            job=self.job,
            applicant=self.applicant,
            cover_letter="Please hire me"
        )

    def test_applicant_can_see_own_applications(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.applicant_token}")    # type: ignore
        response = self.client.get(reverse("applicant-dashboard"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # type: ignore
        self.assertEqual(response.data[0]["job"]["id"], self.job.id)  # type: ignore

    def test_recruiter_can_see_applications_to_their_jobs(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.recruiter_token}")    # type: ignore
        response = self.client.get(reverse("recruiter-dashboard"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # type: ignore
        self.assertEqual(response.data[0]["applicant"]["email"], "applicant@example.com")   # type: ignore
