from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), # Registers a new user
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    # give back access and refresh JWT tokens
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),    # Update access token when given the right refresh token
]
