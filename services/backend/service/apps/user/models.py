from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.user import managers, choises


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=32,
        choices=choises.UserRole.choices,
        default=choises.UserRole.USER
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return f'{self.id} email: {self.email}'
