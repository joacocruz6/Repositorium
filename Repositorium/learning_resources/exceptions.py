from repositorium.utils.exceptions import AlreadyExistsError, DoesNotExistsError


class CategoryException(Exception):
    pass


class CategoryAlreadyExists(CategoryException, AlreadyExistsError):
    pass


class CategoryDoesNotExists(CategoryException, DoesNotExistsError):
    pass


class SystemException(Exception):
    pass


class SystemAlreadyExists(SystemException, AlreadyExistsError):
    pass


class SystemDoesNotExists(SystemException, DoesNotExistsError):
    pass


class LearningObjectException(Exception):
    pass


class LearningObjectDoesNotExists(LearningObjectException, DoesNotExistsError):
    pass


class LearningObjectAlreadyExists(LearningObjectException, AlreadyExistsError):
    pass
