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
from repositorium.recomendations.recomendation_models.recomendation_model import (
    ItemsKNNRecomendationModel,
    UserKNNRecomendationModel,
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

KNN_BASIC_MODEL = RecomendationModel(
    "548e3f29-39d0-4bef-bbcf-b4bb5900785b",
    UserKNNRecomendationModel,
    "User-User collaborative filter with KNN",
    ["548e3f29-39d0-4bef-bbcf-b4bb5900785b"],
    {},
)

KNN_ITEMS_MODEL = RecomendationModel(
    "29c909ac-ccb0-4a0a-9818-a9e0f4833910",
    ItemsKNNRecomendationModel,
    "Item-Item collaborative filter with KNN",
    ["29c909ac-ccb0-4a0a-9818-a9e0f4833910"],
    {},
)

RECOMENDATION_MODELS = {
    "529c758f-9de6-4e25-bbd5-27db8b9f3011": PROFILE_TAGS_MODEL,
    "66c99e25-cdc7-4ed6-8f4c-9d3619898b8b": LAST_CREATED_MODEL,
    "548e3f29-39d0-4bef-bbcf-b4bb5900785b": KNN_BASIC_MODEL,
    "29c909ac-ccb0-4a0a-9818-a9e0f4833910": KNN_ITEMS_MODEL,
}


def get_recomendation_model_by_uuid(uuid: str) -> AbstractRecomendationModel:
    model = RECOMENDATION_MODELS.get(uuid)
    if model is None:
        raise RecomendationModelNotFound
    recomendation_model = model.modelClass(*model.args, **model.kwargs)
    return recomendation_model


def get_all_recomendation_models() -> Dict[str, RecomendationModel]:
    return RECOMENDATION_MODELS
