from django.db import models

from repositorium.utils.models import BaseUUIDModel


class Category(BaseUUIDModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f"Category {self.name}"


class System(BaseUUIDModel):
    name = models.CharField(max_length=150, unique=True)
    creator_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"System {self.name}"


class LearningObject(BaseUUIDModel):
    title = models.CharField(max_length=150, unique=True)
    categories = models.ManyToManyField(to=Category, related_name="learning_objects")
    description = models.CharField(max_length=450, blank=True, null=True)
    content = models.TextField(blank=True)
    forked = models.ForeignKey(
        to="learning_resources.LearningObject",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    creator_email = models.EmailField(db_index=True)
    created_on = models.ForeignKey(
        to=System,
        on_delete=models.DO_NOTHING,
        related_name="learning_objects",
        null=True,
        blank=True,
    )
    used_by = models.ManyToManyField(to="users.User", through="LearningObjectUsage")
    extra_data = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"LearningObject {self.name}"

    @property
    def is_forked(self):
        return self.forked != None


class LearningObjectUsage(BaseUUIDModel):
    user = models.ForeignKey(
        to="users.User", on_delete=models.DO_NOTHING, related_name="has_used"
    )
    learning_object = models.ForeignKey(
        to=LearningObject, on_delete=models.DO_NOTHING, related_name="+"
    )
    used_on = models.ForeignKey(
        to=System,
        on_delete=models.DO_NOTHING,
        related_name="learning_objects_used",
        null=True,
        blank=True,
    )
    # Binary rating, I use the object or I don't


class LearningObjectFile(BaseUUIDModel):
    file_route = models.FilePathField()
    learning_object = models.ForeignKey(
        to=LearningObject, on_delete=models.CASCADE, related_name="files"
    )

    def __str__(self):
        return f"LearningObjectFile at {self.file_route}"
