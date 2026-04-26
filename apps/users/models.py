from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Platform user: administrator or community member."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Administrator"
        COMMUNITY = "community", "Community"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.COMMUNITY,
        db_index=True,
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN
        if self.role == self.Role.ADMIN:
            self.is_staff = True
        elif self.role == self.Role.COMMUNITY and not self.is_superuser:
            self.is_staff = False
        super().save(*args, **kwargs)
