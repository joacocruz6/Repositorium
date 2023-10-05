from typing import Optional

from repositorium.recomendations.exceptions import ExperimentNotFoundError
from repositorium.recomendations.models import Experiment
from repositorium.users.models import User


def create_experiment(user: User) -> Experiment:
    experiment = Experiment.objects.create(user=user)
    return experiment


def get_experiment_by_uuid(uuid: str, user_uuid: str) -> Experiment:
    experiment = Experiment.objects.filter(uuid=uuid, user__uuid=user_uuid).first()
    if experiment is None:
        raise ExperimentNotFoundError
    return experiment


def finish_experiment(
    uuid: str, user_uuid: str, model_uuid: str, item_recommended_uuid: str
):
    try:
        experiment = get_experiment_by_uuid(uuid=uuid, user_uuid=user_uuid)
        experiment.chosen_recomendation = item_recommended_uuid
        experiment.model_chosen = model_uuid
        experiment.save(
            update_fields=["updated_at", "chosen_recomendation", "model_chosen"]
        )
    except ExperimentNotFoundError as e:
        raise e
