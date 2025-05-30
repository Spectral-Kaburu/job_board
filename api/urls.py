from django.urls import path
from .views import RegisterView, UserView, update_profile, AdminUserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), # Registers a new user
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    # give back access and refresh JWT tokens
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),    # Update access token when given the right refresh token
    path('user/', UserView.as_view(), name='user'),
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('update-profile/', update_profile, name='update-profile'),
]
