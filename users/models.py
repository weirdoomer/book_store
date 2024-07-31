from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_verified_email = models.BooleanField(default=False)
