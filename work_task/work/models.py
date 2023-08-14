import django.db.models
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class ProfileManager(models.Manager):
    pass


class Profile(AbstractUser):
    ROLE_CHOICES = [
        ('a', 'administrator'),
        ('w', 'worker'),
        ('u', 'user')
    ]
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='u')
