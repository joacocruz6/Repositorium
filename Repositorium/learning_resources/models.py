from django.db import models
from repositorium.utils.models import BaseUUIDModel

# Create your models here.


class Categories(BaseUUIDModel):
    name = models.CharField(max_length=150)


class System(BaseUUIDModel):
    name = models.CharField(max_length=150)
