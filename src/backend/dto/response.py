from dataclasses import dataclass

from .base import FromModelMixin, ToSchemaMixin


@dataclass(slots=True, frozen=True)
class ExampleResponseDTO(FromModelMixin, ToSchemaMixin):
    example_id: str
    name: str
