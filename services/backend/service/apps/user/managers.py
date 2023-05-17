from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction, models
from apps.user.choises import UserRole


class UserQuerySet(models.QuerySet):
    ...


class CustomUserManager(BaseUserManager):

    def create_user(self, password=None, **kwargs):
        return self._create_user(password, **kwargs)

    def create_superuser(self, password=None, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        kwargs.setdefault('role', UserRole.ADMIN)
        return self._create_user(password, **kwargs)

    @transaction.atomic
    def _create_user(self, password=None, **kwargs):
        user = self.model(**kwargs)

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user


UserManager = CustomUserManager.from_queryset(UserQuerySet)
