from dataclasses import dataclass

from .base import FromSchemaMixin


@dataclass(slots=True, frozen=True)
class CreateRequestDTO(FromSchemaMixin):
    name: str


@dataclass(slots=True, frozen=True)
class UpdateRequestDTO(FromSchemaMixin):
    name: str | None
