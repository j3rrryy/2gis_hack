from dataclasses import dataclass

from .base import FromModelMixin, ToSchemaMixin


@dataclass(slots=True, frozen=True)
class ReadResponseDTO(FromModelMixin, ToSchemaMixin):
    example_id: str
    name: str
