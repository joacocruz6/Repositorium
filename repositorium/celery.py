import os

from celery import Celery
from django.conf import settings

# from .recomendations.recomendation_models.manager import KNN_BASIC_MODEL, KNN_ITEMS_MODEL, get_recomendation_model_by_uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "repositorium.settings")

app = Celery("repositorium")

app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


# @app.task
# def retrain_models(self):
#    knn_basic_model = get_recomendation_model_by_uuid(KNN_BASIC_MODEL.uuid)
#    knn_items_model = get_recomendation_model_by_uuid(KNN_ITEMS_MODEL.uuid)
#    knn_basic_model.train()
#    knn_items_model.train()
