from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession

from dto import request as request_dto
from repository import CalculationRepository
from tasks import calculate


class CalculationService:
    @staticmethod
    async def create_calculation(
        data: request_dto.CreateCalculationRequestDTO, session: AsyncSession
    ) -> str:
        calculation_id = await CalculationRepository.create_calculation(data, session)
        calculate.delay(calculation_id, asdict(data))  # pyright: ignore[reportFunctionMemberAccess]
        return calculation_id
