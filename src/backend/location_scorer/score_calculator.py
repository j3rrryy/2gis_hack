import asyncio
import logging
from typing import Optional

from aiohttp import ClientSession

from .infrastructure_checker import InfrastructureChecker


class ScoreCalculator:
    CATEGORY_BOUNDS = {
        # Транспорт и мобильность
        "метро": [200, 2000],
        "остановка_автобуса": [100, 500],
        "велодорожка": [300, 1500],
        # Образование и развитие
        "детский_сад": [200, 1000],
        "школа": [500, 2000],
        "библиотека": [1000, 3000],
        # Здравоохранение
        "больница": [1000, 5000],
        "поликлиника": [500, 2000],
        "аптека": [300, 1500],
        # Отдых и спорт
        "парк": [300, 1500],
        "спортплощадка": [500, 2000],
        # Покупки и услуги
        "супермаркет": [300, 1500],
        "продуктовый_магазин": [200, 1000],
        "торговый_центр": [1000, 5000],
        # Социальная инфраструктура
        "кафе": [300, 2000],
        "ресторан": [500, 3000],
        "банк": [500, 2500],
        "почта": [1000, 4000],
        # Безопасность
        "отделение_полиции": [1000, 5000],
        "пожарная_часть": [2000, 8000],
        # Культура и развлечения
        "кинотеатр": [1000, 5000],
        "театр": [2000, 10000],
        "музей": [2000, 10000],
        # Специализированные объекты
        "автосервис": [1000, 5000],
        "автомойка": [1000, 5000],
        "строймаркет": [2000, 10000],
    }

    logger = logging.getLogger("ScoreCalculator")

    @classmethod
    async def run(
        cls, coordinate_x: float, coordinate_y: float, client_session: ClientSession
    ) -> dict[str, int]:
        async def calculate_part(inf_type: str, bounds: list[int]) -> Optional[float]:
            try:
                distance = await InfrastructureChecker.check_closest_infrastructure(
                    inf_type, coordinate_x, coordinate_y, client_session
                )
                if distance is None:
                    return

                left_bound, right_bound = bounds[0], bounds[1]

                if distance <= left_bound:
                    points = 10.0
                elif distance >= right_bound:
                    points = 0.0
                else:
                    points = 10.0 * (
                        1 - (distance - left_bound) / (right_bound - left_bound)
                    )
                return points
            except Exception as exc:
                cls.logger.error(str(exc))

        tasks = [
            asyncio.create_task(calculate_part(inf_type, bounds))
            for inf_type, bounds in cls.CATEGORY_BOUNDS.items()
        ]
        results = await asyncio.gather(*tasks)
        valid_results = {
            category.capitalize().replace("_", " "): round(result)
            for category, result in zip(cls.CATEGORY_BOUNDS, results)
            if result is not None
        }

        if not valid_results:
            return {"score": 0}

        score = sum(valid_results.values()) / len(valid_results)
        valid_results["score"] = round(score)
        return valid_results
