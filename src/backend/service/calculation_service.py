from dataclasses import asdict

from cashews import cache
from sqlalchemy.ext.asyncio import AsyncSession

from dto import request as request_dto
from dto import response as response_dto
from repository import CalculationRepository
from tasks import calculate
from utils import get_calculation_key


class CalculationService:
    @staticmethod
    async def create_calculation(
        data: request_dto.CreateCalculationRequestDTO, session: AsyncSession
    ) -> str:
        calculation_id = await CalculationRepository.create_calculation(data, session)
        calculate.delay(calculation_id, asdict(data))  # pyright: ignore[reportFunctionMemberAccess]
        return calculation_id

    @staticmethod
    async def get_calculation(
        calculation_id: str, session: AsyncSession
    ) -> response_dto.CalculationResponseDTO:
        cache_key = get_calculation_key(calculation_id)
        if cached := await cache.get(cache_key):
            return cached

        calculation = await CalculationRepository.get_calculation(
            calculation_id, session
        )

        if calculation.result:
            await cache.set(cache_key, calculation, 3600)
        return calculation
