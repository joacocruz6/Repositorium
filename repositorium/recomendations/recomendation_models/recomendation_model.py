import random

from surprise.prediction_algorithms import knns

from repositorium.learning_resources.managers import (
    learning_objects as learning_object_manager,
)
from repositorium.recomendations.recomendation_models import base
from repositorium.users import managers as user_manager


class UserKNNRecomendationModel(base.AbstractRecomendationModel):
    algo: knns.KNNBasic = None

    def __init__(self):
        super().__init__()
        self.algo = None

    def load(self, *args, **kwargs) -> None:
        pass

    def get_recomendation(self, user_uuid: str, *args, **kwargs) -> LearningObject:
        self.load()
        neighbours = self.algo.get_neighbors(user_uuid, 5)
        users = user_manager.get_users_by_uuid(users_uuid=neighbours)
        learning_objects = list()
        for user in users:
            learning_object = (
                learning_object_manager.get_user_last_used_learning_object(
                    user_email=user.email
                )
            )
            learning_objects.append(learning_object)
        return random.choice(learning_objects)


class ItemsKNNRecomendationModel(UserKNNRecomendationModel):
    def get_recomendation(self, item_uuid: str, *args, **kwargs) -> LearningObject:
        self.load()
        neighbours = self.algo.get_neighbors(item_uuid, 5)
        learning_objects = learning_object_manager.get_learning_objects_by_uuids(
            learning_objects_uuids=neighbours
        )
        return random.choice(learning_objects)
