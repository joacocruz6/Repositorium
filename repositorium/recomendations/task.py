from celery import shared_task

from repositorium.recomendations.recomendation_models.manager import (
    KNN_BASIC_MODEL,
    KNN_ITEMS_MODEL,
    get_recomendation_model_by_uuid,
)


@shared_task
def retrain_models():
    knn_basic_model = get_recomendation_model_by_uuid(KNN_BASIC_MODEL.uuid)
    knn_items_model = get_recomendation_model_by_uuid(KNN_ITEMS_MODEL.uuid)
    knn_basic_model.train()
    knn_items_model.train()
