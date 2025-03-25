"""Module providing a Custom User."""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    """Class representing a Custiom User Manager."""

    def create_user(self, email, name, gender, password=None):
        """Function creating user."""

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            gender=gender,
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, gender, password=None):
        """Function creating superuser."""

        user = self.create_user(
            email=email,
            password=password,
            name=name,
            gender=gender,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Class representing a Custom User model."""

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'gender']

    def __str__(self):
        return str(self.email)
