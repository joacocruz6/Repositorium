from django.core.exceptions import ObjectDoesNotExist


class AlreadyExistsError(Exception):
    pass


class DoesNotExistsError(ObjectDoesNotExist):
    pass
