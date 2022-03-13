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
    created_by = models.ForeignKey(
        to="users.User", on_delete=models.DO_NOTHING, related_name="learning_objects"
    )
    created_on = models.ForeignKey(
        to=System,
        on_delete=models.DO_NOTHING,
        related_name="learning_objects",
        null=True,
        blank=True,
    )
    used_by = models.ManyToManyField(to="users.User", through="Ratings")
    extra_data = models.JSONField(default=dict, null=True, blank=True)


class Ratings(BaseUUIDModel):
    user = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, related_name="ratings"
    )
    learning_object = models.ForeignKey(
        to=LearningObject, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
