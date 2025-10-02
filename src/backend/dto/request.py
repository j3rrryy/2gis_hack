from dataclasses import dataclass

from .base import FromSchemaMixin


@dataclass(slots=True, frozen=True)
class CreateRequestDTO(FromSchemaMixin):
    name: str
