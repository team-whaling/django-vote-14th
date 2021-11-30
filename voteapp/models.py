from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    voted = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'


class Candidate(models.Model):
    name = models.CharField(max_length=30)
    vote = models.IntegerField(default=0)

    class Meta:
        db_table = 'candidate'
        ordering = ['-vote', 'name']
