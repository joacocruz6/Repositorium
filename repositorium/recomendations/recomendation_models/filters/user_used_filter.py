from django.db.models import QuerySet

from repositorium.learning_resources.models import LearningObject, LearningObjectUsage
from repositorium.recomendations.recomendation_models.filters import base


class UserSeenFilter(base.AbstractFilter):
    def get_objects(self, user_uuid: str, *args, **kwargs) -> QuerySet:
        learning_object_uuids = LearningObjectUsage.objects.filter(
            user__uuid=user_uuid
        ).values_list("learning_object__uuid", flat=True)
        used_learning_objects = LearningObject.objects.filter(
            uuid__in=learning_object_uuids
        )  # Obtain all the LO used by the user
        tags = set()  # Obtain the tags of them, non repeated
        for learning_object in used_learning_objects:
            lo_tags = learning_object.categories.values_list("name", flat=True)
            for tag_name in lo_tags:
                tags.add(tag_name)
        return LearningObject.objects.filter(
            categories__name__in=tags
        )  # Obtain all the seen tags of them
