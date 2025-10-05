from pydantic import BaseModel, Field
from typing import List, Union

class LocationDto(BaseModel):
    geometry_id: str | None = Field(default=None)
    id: str | None = Field(default=None)
    is_advertising: bool = Field(default=False)
    lat: float = Field(default=55.736483)
    lon: float = Field(default=37.589985)
    match_type: int = Field(default=0)
    rubr: str | None = Field(default=None)
    source_type: int = Field(default=0)
    type: str | None = Field(default=None)
    vital: int = Field(default=0)

class PointDto(BaseModel):
    type: str = Field(default='stop')
    lat: float | None = Field(default=55.736483)
    lon: float | None = Field(default=37.589985)

class RoutingRequestDto(BaseModel):
    points: List[PointDto] = Field(default=[])
    locale: str = Field(default="ru")
    transport: str = Field(default="driving")
    route_mode: str = Field(default="fastest")
    traffic_mode: str = Field(default="jam")