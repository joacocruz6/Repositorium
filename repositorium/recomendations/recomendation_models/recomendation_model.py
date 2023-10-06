import random
from typing import Dict, List

import pandas as pd
from surprise import Dataset, Reader, dump
from surprise.dataset import DatasetAutoFolds
from surprise.model_selection import cross_validate
from surprise.prediction_algorithms import knns
from surprise.prediction_algorithms.algo_base import AlgoBase

from repositorium.learning_resources.managers import (
    learning_object_usage as learning_object_usage_manager,
)
from repositorium.learning_resources.managers import (
    learning_objects as learning_object_manager,
)
from repositorium.learning_resources.models import LearningObject
from repositorium.recomendations.recomendation_models import base
from repositorium.users import managers as user_manager


class SurpriseAlgorithm(object):
    algo: AlgoBase = None
    sim_options: Dict = None
    algo_class: type = None

    def get_algo_class(self) -> type:
        if self.algo_class is None:
            raise Exception
        return self.algo_class

    def get_path(self) -> str:
        if self.path is None:
            raise Exception
        return self.path

    def get_sim_options(self) -> Dict:
        if self.sim_options is None:
            raise Exception
        return self.sim_options

    def is_used_by_user(self, learning_object_uuid: str, user_email: str, lous) -> bool:
        for lou in lous:
            if (
                lou["user_id"] == user_email
                and lou["learning_object_id"] == learning_object_uuid
            ):
                return True
        return False

    def create_rating_mapping(
        self, users: List, learning_objects: List, learning_object_usage: List
    ) -> Dict:
        users_ids = list()
        learning_objects_ids = list()
        usage = list()
        for user in users:
            user_id = user["uuid"]
            user_email = user["email"]
            user_lous = list()
            user_lous_uuids = list()
            for learning_object_uuid in learning_objects:
                user_lous_uuids.append(learning_object_uuid)
                if self.is_used_by_user(
                    learning_object_uuid, user_email, learning_object_usage
                ):
                    user_lous.append(1)
                else:
                    user_lous.append(0)
            users_ids.extend([user_id for _ in user_lous_uuids])
            learning_objects_ids.extend(user_lous_uuids)
            usage.extend(user_lous)
        data = {
            "userUUID": users_ids,
            "learningObjectUUID": learning_objects_ids,
            "rating": usage,
        }
        return data

    def get_and_build_dataset(self) -> DatasetAutoFolds:
        users = list(user_manager.get_all_users().values("email", "uuid"))
        learning_objects = list(
            learning_object_manager.get_all_learning_objects().values_list(
                "uuid", flat=True
            )
        )
        learning_objects_usage = list(
            learning_object_usage_manager.get_all_learning_object_usage().values(
                "user_id", "learning_object_id"
            )
        )
        mapping_data = self.create_rating_mapping(
            users, learning_objects, learning_objects_usage
        )
        df = pd.DataFrame(mapping_data)
        df = df.sample(frac=1)
        train_set = df[["userUUID", "learningObjectUUID", "rating"]]
        reader = Reader(rating_scale=(0, 1))
        return Dataset.load_from_df(train_set, reader)

    def train(self) -> None:
        dataset = self.get_and_build_dataset()
        sim_options = self.get_sim_options()
        self.algo = self.get_algo_class()(sim_options=sim_options)
        cross_validate(self.algo, dataset, cv=4)
        self.save()

    def save(self) -> None:
        path = self.get_path()
        dump.dump(path, algo=self.algo)


class UserKNNRecomendationModel(SurpriseAlgorithm, base.AbstractRecomendationModel):
    predictor: knns.KNNBasic = None
    sim_options = {"user_based": True}
    algo_class = knns.KNNBasic

    def __init__(self, uuid):
        super().__init__()
        self.uuid = uuid
        self.path = f"RecomendationModels/{self.uuid}.sav"

    def get_top_n(self, uuid: str, n=5) -> List[str]:
        learning_objects = list(
            learning_object_manager.get_all_learning_objects().values_list(
                "uuid", flat=True
            )
        )
        if len(learning_objects) <= n:
            return learning_objects
        top_n = list()  # uuid, rating
        for learning_object_uuid in learning_objects:
            prediction = self.algo.predict(uuid, learning_object_uuid)
            rating_predicted = prediction.est
            if len(top_n) < n:
                top_n.append((learning_object_uuid, rating_predicted))
            else:
                min_index = 0
                _, min_seen_so_far = top_n[0]
                for i in range(len(top_n)):
                    _, rating = top_n[i]
                    if rating < min_seen_so_far:
                        min_seen_so_far = rating
                        min_index = i
                if min_seen_so_far < rating_predicted:
                    top_n[min_index] = (learning_object_uuid, rating_predicted)
        top_n_uuid = [lo_uuid for lo_uuid, _ in top_n]
        return top_n_uuid

    def load(self, *args, **kwargs) -> None:
        _, self.predictor = dump.load(self.get_path())

    def get_recomendation(self, user_uuid: str, *args, **kwargs) -> LearningObject:
        self.load()
        neighbours = self.get_top_n(user_uuid, n=5)
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
    sim_options = {"user_based": False}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_recomendation(self, item_uuid: str, *args, **kwargs) -> LearningObject:
        self.load()
        dataset = self.get_and_build_dataset()
        trainset = dataset.build_full_trainset()
        item_id = trainset.to_inner_iid(item_uuid)
        neighbours = self.predictor.get_neighbors(item_id, 5)
        neighbours_uuids = [
            trainset.to_raw_iid(neighbour_id) for neighbour_id in neighbours
        ]
        learning_objects = learning_object_manager.get_learning_objects_by_uuids(
            learning_objects_uuids=neighbours_uuids
        )
        return random.choice(learning_objects)
