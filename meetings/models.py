from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .service import set_watermark, avatar_file_name


class User(AbstractUser):

    class Sex(models.TextChoices):
        MAN = "m", "Man"
        WOMAN = "w", "Woman"

    sex = models.CharField(max_length=1, choices=Sex.choices, default=Sex.MAN)
    avatar = models.ImageField(upload_to=avatar_file_name, null=True, blank=True)
    liked_users = models.ManyToManyField(
        "self", related_name="users_liked_me", symmetrical=False, blank=True, null=True
    )
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            watermark_path = f'{settings.MEDIA_ROOT}/docker.png'
            set_watermark(self.avatar, watermark_path)
