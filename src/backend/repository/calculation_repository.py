from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dto import request as request_dto
from dto import response as response_dto

from .models import Calculation


class CalculationRepository:
    @staticmethod
    async def create_calculation(
        data: request_dto.CreateCalculationRequestDTO, session: AsyncSession
    ) -> str:
        new_calculation = data.to_model(Calculation)
        session.add(new_calculation)
        await session.commit()
        await session.refresh(new_calculation)
        return new_calculation.calculation_id

    @staticmethod
    async def get_calculation(
        calculation_id: str, session: AsyncSession
    ) -> response_dto.CalculationResponseDTO:
        calculation = await session.get(Calculation, calculation_id)
        if not calculation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Calculation not found",
            )
        return response_dto.CalculationResponseDTO.from_model(calculation)
