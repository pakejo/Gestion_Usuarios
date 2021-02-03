from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """Model definition for User"""
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    genre = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    codlogin = models.CharField(max_length=6, blank=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        """Meta definition for User"""
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.name + ' ' + self.surname
