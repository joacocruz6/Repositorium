import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

# Create your models here.


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(primary_key=True, unique=True)
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = UserManager()

    @property
    def full_name(self):
        return self.first_name + self.last_name

    def __str__(self):
        return f"User {self.email}"
