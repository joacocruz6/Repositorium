class CategoryException(Exception):
    pass


class CategoryAlreadyExists(CategoryException):
    pass


class CategoryDoesNotExists(CategoryException):
    pass


class SystemException(Exception):
    pass


class SystemAlreadyExists(SystemException):
    pass


class SystemDoesNotExists(SystemException):
    pass
