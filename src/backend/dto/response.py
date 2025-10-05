from dataclasses import dataclass
from datetime import datetime

from .base import FromModelMixin, ToSchemaMixin


@dataclass(slots=True, frozen=True)
class CalculationResponseDTO(FromModelMixin, ToSchemaMixin):
    result: int | None
    status: str
    scheduled_at: datetime
    calculated_at: datetime | None
