import os
import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


def photo_path(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    chars = string.ascii_lowercase
    randomstring = ''.join((random.choice(chars)) for x in range(12))
    return f'avatars/{randomstring}{file_extension}'


class DaterUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    avatar = models.ImageField(upload_to=photo_path)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    match = models.ManyToManyField('self', blank=True, symmetrical=False)
    longitude = models.FloatField(
        null=True, validators=[MinValueValidator(-180), MaxValueValidator(180)], blank=True)
    latitude = models.FloatField(null=True, validators=[
                                 MinValueValidator(-90), MaxValueValidator(90)], blank=True)

    def __str__(self):
        return self.username
