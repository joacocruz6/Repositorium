from repositorium.learning_resources.models import System
from repositorium.learning_resources.exceptions import (
    SystemAlreadyExists,
    SystemDoesNotExists,
)


def system_exists(name: str) -> bool:
    return System.objects.filter(name=name).exists()


def create_system(name: str) -> System:
    if system_exists(name=name):
        raise SystemAlreadyExists
    return System.objects.create(name=name)


def get_system_by_name(name: str) -> System:
    pass
