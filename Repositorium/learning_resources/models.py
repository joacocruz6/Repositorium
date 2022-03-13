from django.db import models
from repositorium.utils.models import BaseUUIDModel

# Create your models here.


class Categories(BaseUUIDModel):
    name = models.CharField(max_length=150)


class System(BaseUUIDModel):
    name = models.CharField(max_length=150)


class LearningObject(BaseUUIDModel):
    name = models.CharField(max_length=150)
    categories = models.ManyToManyField(to=Categories, related_name="learning_objects")
    content = models.TextField()
    forked = models.ForeignKey(
        to="learning_resources.LearningObject",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(to="users.User", on_delete=models.DO_NOTHING)
