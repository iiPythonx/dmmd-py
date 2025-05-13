# Copyright (c) 2025 iiPython

# Modules
import typing

from dmmd.client import Client

# Main class
class Static:
    def __init__(self, base_url: str = "https://static.dmmdgm.dev") -> None:
        self.client = Client(base_url)

    # Endpoint handlers
    async def file(self, scope: str, path: str, token: typing.Optional[str] = None) -> bytes:
        return await self.client.request(
            f"/files/{scope}/{path}",
            params = {"token": token} if token is not None else {}
        )
