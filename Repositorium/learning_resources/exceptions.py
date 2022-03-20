class CategoryException(Exception):
    pass


class CategoryAlreadyExists(CategoryException):
    pass


class CategoryDoesNotExists(CategoryException):
    pass
