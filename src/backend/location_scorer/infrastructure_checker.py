import logging
import os
from typing import Any, Optional

from aiohttp import ClientSession

from .location_scorer_external import LocationScorerExternal


class InfrastructureChecker:
    BASE_MARKERS_URL = "https://catalog.api.2gis.com/3.0/markers"
    BASE_ROUTING_URL = "https://routing.api.2gis.com/routing/7.0.0/global"
    API_KEY = os.environ["API_KEY"]

    logger = logging.getLogger("InfrastructureChecker")

    @classmethod
    async def check_closest_infrastructure(
        cls,
        infra_type: str,
        coordinate_x: float,
        coordinate_y: float,
        client_session: ClientSession,
    ) -> Optional[int]:
        adjusted_coords = cls._adjust_coordinates(coordinate_x, coordinate_y)
        data = await LocationScorerExternal.get_request(
            cls.BASE_MARKERS_URL,
            {
                "q": infra_type,
                "point": f"{adjusted_coords[1]},{adjusted_coords[0]}",
                "radius": 1000,
                "sort": "distance",
                "key": cls.API_KEY,
            },
            client_session,
        )
        if not (first_item := cls._parse_first_item(data)):
            return
        route = await LocationScorerExternal.post_request(
            cls.BASE_ROUTING_URL,
            {"key": cls.API_KEY},
            {
                "points": [
                    {
                        "type": "walking",
                        "lat": first_item["lat"],
                        "lon": first_item["lon"],
                    },
                    {
                        "type": "walking",
                        "lat": adjusted_coords[0],
                        "lon": adjusted_coords[1],
                    },
                ],
                "locale": "ru",
                "transport": "walking",
            },
            client_session,
        )
        return cls._get_route_length(route)

    @classmethod
    def _get_route_length(cls, route: dict[str, Any]) -> Optional[int]:
        try:
            results = route["result"]
            if not results:
                return
            first_route = results[0]
            if "total_distance" in first_route:
                return first_route["total_distance"]
            elif "ui_total_distance" in first_route:
                ui_distance = first_route["ui_total_distance"]
                if "value" in ui_distance:
                    try:
                        return int(ui_distance["value"])
                    except Exception as exc:
                        cls.logger.error(str(exc))
                        raise
            else:
                total_from_maneuvers = cls._sum_maneuvers_distance(first_route)
                if total_from_maneuvers:
                    return total_from_maneuvers
            return
        except Exception:
            return

    @classmethod
    def _sum_maneuvers_distance(cls, route: dict[str, Any]) -> Optional[int]:
        try:
            if "maneuvers" not in route:
                return

            total_distance = 0
            for maneuver in route["maneuvers"]:
                if (
                    "outcoming_path" in maneuver
                    and "distance" in maneuver["outcoming_path"]
                ):
                    total_distance += maneuver["outcoming_path"]["distance"]

            return total_distance if total_distance > 0 else None
        except Exception as exc:
            cls.logger.error(str(exc))
            raise

    @classmethod
    def _parse_first_item(cls, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        try:
            items = data.get("result", {}).get("items", [])
            if not items:
                return
            return {"lat": items[0]["lat"], "lon": items[0]["lon"]}
        except Exception as exc:
            cls.logger.error(str(exc))
            raise

    @staticmethod
    def _adjust_coordinates(
        coordinate_x: float, coordinate_y: float
    ) -> tuple[float, float]:
        if coordinate_x <= -180:
            coordinate_x = -179.999
        elif coordinate_x >= 180:
            coordinate_x = 179.999

        if coordinate_y <= -90:
            coordinate_y = -89.999
        elif coordinate_y >= 90:
            coordinate_y = 89.999
        return coordinate_x, coordinate_y
