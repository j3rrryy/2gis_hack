from pydantic import BaseModel, Field


class CreateCalculationRequestSchema(BaseModel):
    coordinate_x: float = Field(..., ge=-180, le=180)
    coordinate_y: float = Field(..., ge=-90, le=90)


class CreateCalculationResponseSchema(BaseModel):
    calculation_id: str
