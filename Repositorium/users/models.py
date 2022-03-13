from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

# Create your models here.


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    systems = models.ManyToManyField(
        to="learning_resources.System", related_name="users"
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    @property
    def full_name(self):
        return self.first_name + self.last_name
