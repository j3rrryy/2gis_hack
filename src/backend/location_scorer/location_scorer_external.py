import logging
from typing import Any

from aiohttp import ClientSession


class LocationScorerExternal:
    logger = logging.getLogger("LocationScorerExternal")

    @classmethod
    async def get_request(
        cls, url: str, params: dict[str, Any], client_session: ClientSession
    ) -> dict[str, Any]:
        try:
            async with client_session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as exc:
            cls.logger.error(str(exc))
            raise

    @classmethod
    async def post_request(
        cls,
        url: str,
        params: dict[str, Any],
        data: dict[str, Any],
        client_session: ClientSession,
    ) -> dict[str, Any]:
        try:
            async with client_session.post(
                url,
                params=params,
                data=data,
                headers={"Content-Type": "application/json"},
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as exc:
            cls.logger.error(str(exc))
            raise
