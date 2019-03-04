from django.core.management.base import BaseCommand
from authapp.models import CustomUser
from authapp.models import CustomUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = CustomUser.objects.all()
        for user in users:
            users_profile = CustomUserProfile.objects.create(user=user)
            users_profile.save()
