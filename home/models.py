from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    steam_id = models.CharField(default='', blank=True, max_length=20)

    class Meta:
        permissions = (
            ("access_uploader", "Can access the uploader"),
            ("uploader_advanced", "Has access to the advanced uploader options")
        )
