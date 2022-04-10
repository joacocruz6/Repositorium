from django.db import models

from repositorium.utils.models import BaseUUIDModel


class Category(BaseUUIDModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f"Category {self.name}"


class System(BaseUUIDModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f"System {self.name}"


class LearningObject(BaseUUIDModel):
    name = models.CharField(max_length=150, unique=True)
    categories = models.ManyToManyField(to=Category, related_name="learning_objects")
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

    def __str__(self):
        return f"LearningObject {self.name}"

    @property
    def is_forked(self):
        return self.forked != None


class Ratings(BaseUUIDModel):
    user = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, related_name="ratings"
    )
    learning_object = models.ForeignKey(
        to=LearningObject, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)