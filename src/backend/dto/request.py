from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from geoalchemy2 import WKTElement

from .base import FromSchemaMixin, Model, ToModelMixin

if TYPE_CHECKING:
    from repository import Calculation


@dataclass(slots=True, frozen=True)
class CreateCalculationRequestDTO(FromSchemaMixin, ToModelMixin):
    coordinate_x: float
    coordinate_y: float

    def to_model(self, model: type[Model]) -> Model:
        _model = cast("Calculation", model)
        wkt_point = f"POINT({self.coordinate_x} {self.coordinate_y})"
        coordinate = WKTElement(wkt_point, srid=4326)
        return _model(coordinate=coordinate)
