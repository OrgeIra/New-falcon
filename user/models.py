from django.db import models
from django.contrib.auth.models import AbstractUser
from user.managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField("Email Address", unique=True)

    phone = models.CharField(max_length=20, blank=True, null=True)  # Add phone
    address = models.TextField(blank=True, null=True)  # Add address
    created_at = models.DateTimeField(auto_now_add=True)  # Add created_at

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
