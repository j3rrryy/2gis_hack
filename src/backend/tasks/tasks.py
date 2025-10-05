from datetime import datetime

import uvloop
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from di import ClientSessionManager, SessionManager
from enums import CalculationStatus
from exceptions import CalculationNotFound
from location_scorer import ScoreCalculator
from repository import Calculation

from .celery_app import celery_app


@celery_app.task(
    autoretry_for=(Exception,),
    max_retries=1,
    default_retry_delay=30,
    soft_time_limit=180,
    time_limit=210,
)
def calculate(calculation_id: str, data: dict[str, float]) -> None:
    async def wrapper() -> None:
        # setup resources
        await SessionManager.setup()
        await ClientSessionManager.setup()

        @SessionManager.run_with_session
        @ClientSessionManager.run_with_client_session
        async def _calculate(
            *, session: AsyncSession, client_session: ClientSession
        ) -> None:
            calculation = await session.get(Calculation, calculation_id)

            if calculation is None:
                raise CalculationNotFound(f"Calculation {calculation_id} not found")

            calculation.status = CalculationStatus.PROCESSING.value
            await session.commit()

            try:
                result = await ScoreCalculator.run(
                    data["coordinate_x"], data["coordinate_y"], client_session
                )
            except Exception:
                calculation.status = CalculationStatus.FAILED.value
                await session.commit()
                raise

            calculation.result = result
            calculation.calculated_at = datetime.now()
            calculation.status = CalculationStatus.COMPLETED.value
            await session.commit()

        await _calculate()  # pyright: ignore[reportCallIssue]

        # cleanup resources
        await ClientSessionManager.close()
        await SessionManager.close()

    uvloop.run(wrapper())
