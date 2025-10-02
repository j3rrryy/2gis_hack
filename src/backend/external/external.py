from typing import Any

from aiohttp import ClientSession


class ExampleExternal:
    @staticmethod
    async def external_api_example(client_session: ClientSession) -> dict[str, Any]:
        async with client_session.get("https://catfact.ninja/fact") as r:
            return await r.json()
