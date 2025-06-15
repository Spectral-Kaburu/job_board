from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):     # Manages how users are created
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email) # Makes the email lowercase
        user = self.model(email=email, **extra_fields) # creates user object
        user.set_password(password) # Hashes the password
        user.save(using=self._db)   # saves user in the database
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):   # Creates admin user
        extra_fields.setdefault("is_staff", True)   # Can log into admin
        extra_fields.setdefault("is_superuser", True)   # Has all power

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)   # Is the user allowed to log in?
    is_staff = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager() # Tells django to use UserManager when creating users

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email

