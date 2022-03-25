from uuid import UUID
from typing import Tuple, Union
from django.db.models import QuerySet
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
    system = System.objects.filter(name=name).first()
    if system is None:
        raise SystemDoesNotExists
    return system


def get_system_by_uuid(uuid: Union[str, UUID]) -> System:
    system = System.objects.filter(uuid=uuid).first()
    if system is None:
        raise SystemDoesNotExists
    return system


def get_or_create_system(name: str) -> Tuple[System, bool]:
    return System.objects.get_or_create(name=name)


def get_all_systems() -> QuerySet:
    return System.objects.all()
