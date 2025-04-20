# Copyright (c) 2025 iiPython

# Modules
import json
import typing
import atexit
import asyncio

from aiohttp import ClientSession

from dmmd.exceptions import BadRequest, NotFound, ServerError

# Singleton
class Client:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

        # This is manually typed so I only have to ignore it once
        # rather then on every endpoint because pyright is retarded.
        self._client: ClientSession = None  # type: ignore

    async def _close_client(self) -> None:
        if self._client is not None:
            await self._client.close()

    async def _ensure_client(self) -> None:
        def cleanup() -> None:
            asyncio.run(self._close_client())

        if self._client is None:
            self._client = ClientSession(self._base_url)
            atexit.register(cleanup)

    async def request(self, endpoint: str, **kwargs) -> bytes:
        await self._ensure_client()
        async with self._client.request(
            "POST" if "data" in kwargs else "GET", endpoint,
            **kwargs
        ) as response:
            match response.status:
                case 200:
                    return await response.read()

                case 400:
                    raise BadRequest(await response.text())

                case 404:
                    raise NotFound(endpoint)

                case _ as code:
                    raise ServerError(f"Unexpected response status received: {code}")

    async def json(self, endpoint: str, **kwargs) -> typing.Any:
        response = await self.request(endpoint, **kwargs)
        return json.loads(response.decode())
