from sqlalchemy.ext.asyncio import AsyncSession

from dto import request as request_dto

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
