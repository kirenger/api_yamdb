from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from .validators import validate_email


CHOICES = (
    (settings.USER, 'user'),
    (settings.MODERATOR, 'moderator'),
    (settings.ADMIN, 'admin'),
)


class User(AbstractUser):
    """Модель для работы с пользователями."""
    username = models.CharField(
        max_length=150, unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+')]
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=254,
        unique=True,
        validators=[validate_email]
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=15,
        choices=CHOICES,
        default=settings.USER
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == settings.ADMIN

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR

    def __str__(self) -> str:
        return self.username
