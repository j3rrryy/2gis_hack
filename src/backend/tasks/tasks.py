from datetime import datetime

import uvloop
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from di import ClientSessionManager, SessionManager
from exceptions import CalculationNotFound
from repository import Calculation

from .celery_app import celery_app


@celery_app.task(
    autoretry_for=(Exception,),
    max_retries=1,
    default_retry_delay=30,
    soft_time_limit=300,
    time_limit=330,
)
def calculate(calculation_id: str, data: dict[str, float]) -> None:
    @SessionManager.run_with_session
    @ClientSessionManager.run_with_client_session
    async def wrapper(*, session: AsyncSession, client_session: ClientSession) -> None:
        calculation = await session.get(Calculation, calculation_id)

        if calculation is None:
            raise CalculationNotFound(f"Calculation {calculation_id} not found")

        try:
            ...
        except Exception:
            calculation.is_failed = True
            await session.commit()
            raise

        calculation.is_ready = True
        calculation.is_failed = False
        calculation.calculated_at = datetime.now()
        await session.commit()

    uvloop.run(wrapper())  # pyright: ignore[reportCallIssue]
