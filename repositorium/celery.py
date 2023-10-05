import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "repositorium.settings")

app = Celery("repositorium")

app.config_from_object("django.conf:settings", namespace="CELERY")

# app.conf.beat_schedule = {
#     "debug-task-every-second": {
#         "task": "repositorium.celery.debug_task",
#         "schedule": 1.0,
#     },
#     "retrain-models": {
#         "task": "recomendations.task.retrain_models",
#         "schedule": 60.0,
#     }
# }

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
