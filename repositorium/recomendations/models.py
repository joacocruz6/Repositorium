from django.db import models

from repositorium.utils import models as base_models


# Create your models here.
class Experiment(base_models.BaseUUIDModel):
    user = models.ForeignKey(
        to="users.User", on_delete=models.DO_NOTHING, related_name="experiments"
    )
    chosen_recomendation = models.UUIDField()
