from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
from jobs.models import Job
from applications.models import Application
from rest_framework_simplejwt.tokens import RefreshToken


class AuthTests(APITestCase):
    def test_user_registration_and_login(self):
        # Register
        url = reverse('register')
        user_data = {
            "email": "testuser@example.com",
            "password": "strongpassword123",
            "first_name": "Test",
            "last_name": "User",
            "role": "user"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Login
        login_url = reverse('token_obtain_pair')
        login_data = {
            "email": "testuser@example.com",
            "password": "strongpassword123"
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data) # type: ignore


class JobTests(APITestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(  # type: ignore
            email="recruiter@example.com",
            password="password123",
            is_recruiter=True
        )
        self.token = RefreshToken.for_user(self.recruiter).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")  # type: ignore

    def test_create_job_as_recruiter(self):
        url = reverse('job-list-create')  # your jobs endpoint
        job_data = {
            "title": "Backend Dev",
            "description": "Awesome role",
            "location": "Remote",
            "company":"LomiTech"
        }
        response = self.client.post(url, job_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_job_as_applicant_forbidden(self):
        applicant = User.objects.create_user(   # type: ignore
            email="applicant@example.com",
            password="password123",
            is_recruiter=False
        )
        token = RefreshToken.for_user(applicant).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")   # type: ignore

        url = reverse('job-list-create')
        job_data = {
            "title": "Backend Dev",
            "description": "Not allowed",
            "location": "Mars",
            "company":"LomiTech"     
        }
        response = self.client.post(url, job_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ApplicationTests(APITestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(  # type: ignore
            email="recruiter@example.com", password="password", is_recruiter=True
        )
        self.job = Job.objects.create(
            title="Test Job",
            description="Job Desc",
            location="Anywhere",
            company="LomiTech",
            posted_by=self.recruiter
        )

        self.applicant = User.objects.create_user(  # type: ignore
            email="applicant@example.com", password="password", is_recruiter=False
        )
        self.token = RefreshToken.for_user(self.applicant).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")  # type: ignore

    def test_apply_to_job(self):
        url = reverse('application-list-create')  # or whatever you called it
        with open("resume.txt", "w") as f:
            f.write("Test Resume")

        with open("resume.txt", "rb") as f:
            response = self.client.post(url, {
                "job": self.job.id, # type: ignore
                "cover_letter": "I want this job.",
                "resume": f
            }, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
