from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class BaseUserManager(UserManager):
    """Manager for the User model."""

    def create_superuser(self, email, password, **extra_fields):
        """Assigns email to username field"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, email, password, **extra_fields)


class BaseUser(AbstractUser):
    """User model for the app."""

    email = models.EmailField("email address", unique=True)
    avatar = models.ImageField()
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=10, null=True, default=None)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
