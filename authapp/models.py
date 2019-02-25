from django.db import models
from django.contrib.auth.models import AbstractUser


def image_path(instance, filename):
    return f'users_avatars/{instance.username.lower()}/{filename}'


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=image_path,
                               blank=True,
                               default=''
                               )
    age = models.PositiveIntegerField(verbose_name='возраст')
