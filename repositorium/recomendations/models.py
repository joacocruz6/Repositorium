from django.db import models

from repositorium.utils import models as base_models


# Create your models here.
class Experiment(base_models.BaseUUIDModel):
    user = models.ForeignKey(
        to="users.User", on_delete=models.DO_NOTHING, related_name="experiments"
    )
    chosen_recomendation = models.UUIDField(null=True, default=None)
    model_chosen = models.UUIDField(null=True, default=None)

    @property
    def is_finished(self):
        return self.model_chosen is not None and self.chosen_recomendation is not None
