# Copyright (c) 2025 iiPython

# Modules
import typing
import atexit
import asyncio

from aiohttp import ClientSession

from dmmd.exceptions import EXCEPTION_MAP, ServerException

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

    async def request(self, endpoint: str, **kwargs) -> typing.Any:
        await self._ensure_client()
        async with self._client.request(
            "POST" if "data" in kwargs else "GET", endpoint,
            **kwargs
        ) as response:
            json = await response.json()
            if response.status != 200:
                if json["code"] in EXCEPTION_MAP:
                    raise EXCEPTION_MAP[json["code"]](json["message"])

                raise ServerException(
                    "Received unknown error from server! " +
                    f"{json['code']}: {json['message']}"
                )

            return json
