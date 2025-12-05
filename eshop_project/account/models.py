from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class user(AbstractUser):
    avatar = models.CharField(max_length=20, null=True, blank=True)
    email_active_code = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.get_full_name()
