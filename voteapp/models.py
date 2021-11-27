from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=128, unique=True)

    class Meta:
        db_table = 'user'


class Candidate(models.Model):
    name = models.CharField(max_length=30)
    vote = models.IntegerField()

    class Meta:
        db_table = 'candidate'
        ordering = ['-vote']