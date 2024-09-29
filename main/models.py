from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from main.managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]


class Dictionary(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    language1 = models.CharField(max_length=30)
    language2 = models.CharField(max_length=30)
