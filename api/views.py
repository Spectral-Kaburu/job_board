from rest_framework import generics
from .serializers import RegisterSerializer
from users.models import User
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView): # handles POST requests
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny] # anyone can access
