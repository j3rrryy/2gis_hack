from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from di import SessionManager
from dto import request as request_dto
from schemas import (
    CalculationSchema,
    CreateCalculationRequestSchema,
    CreateCalculationResponseSchema,
)
from service import CalculationService

router = APIRouter(prefix="/calculation", tags=["calculation"])


@router.post("/", status_code=202, response_model=CreateCalculationResponseSchema)
async def create_calculation(
    data: CreateCalculationRequestSchema,
    session: AsyncSession = Depends(SessionManager.session_factory),
) -> CreateCalculationResponseSchema:
    dto = request_dto.CreateCalculationRequestDTO.from_schema(data)
    calculation_id = await CalculationService.create_calculation(dto, session)
    return CreateCalculationResponseSchema(calculation_id=calculation_id)


@router.get("/{calculation_id}", response_model=CalculationSchema)
async def get_calculation(
    calculation_id: UUID,
    session: AsyncSession = Depends(SessionManager.session_factory),
) -> CalculationSchema:
    calculation = await CalculationService.get_calculation(str(calculation_id), session)
    return calculation.to_schema(CalculationSchema)
