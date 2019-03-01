from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


def image_path(instance, filename):
    return f'users_avatars/{instance.username.lower()}/{filename}'


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=image_path,
                               blank=True,
                               default=''
                               )
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

