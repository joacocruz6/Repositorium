from dataclasses import dataclass
from typing import Any, Dict, List

from repositorium.recomendations.recomendation_models.base import (
    AbstractRecomendationModel,
)
from repositorium.recomendations.recomendation_models.basic import (
    SimpleLastCreatedRecomendation,
)
from repositorium.recomendations.recomendation_models.basic_filter import (
    ProfileLastFilteredModel,
)


@dataclass
class RecomendationModel(object):
    uuid: str
    modelClass: type
    description: str
    args: List[Any]
    kwargs: Dict[str, Any]


class RecomendationModelNotFound(Exception):
    pass


LAST_CREATED_MODEL = RecomendationModel(
    "66c99e25-cdc7-4ed6-8f4c-9d3619898b8b",
    SimpleLastCreatedRecomendation,
    "Get the latest LearningObject of the database",
    [],
    {},
)
PROFILE_TAGS_MODEL = RecomendationModel(
    "529c758f-9de6-4e25-bbd5-27db8b9f3011",
    ProfileLastFilteredModel,
    "Get the latest LearningObject from the ones that the user has seen so far",
    [],
    {},
)


RECOMENDATION_MODELS = {
    "529c758f-9de6-4e25-bbd5-27db8b9f3011": PROFILE_TAGS_MODEL,
    "66c99e25-cdc7-4ed6-8f4c-9d3619898b8b": LAST_CREATED_MODEL,
}


def get_recomendation_model_by_uuid(uuid: str) -> AbstractRecomendationModel:
    model = RECOMENDATION_MODELS.get(uuid)
    if model is None:
        raise RecomendationModelNotFound
    recomendation_model = model.modelClass(*model.args, **model.kwargs)
    return recomendation_model


def get_all_recomendation_models() -> Dict[str, RecomendationModel]:
    return RECOMENDATION_MODELS
