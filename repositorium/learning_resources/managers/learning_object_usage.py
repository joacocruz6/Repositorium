from django.db.models import QuerySet

from repositorium.learning_resources.models import LearningObjectUsage


def get_all_learning_object_usage() -> QuerySet:
    return LearningObjectUsage.objects.all()
