# Copyright (c) 2025 iiPython

# Modules
from dmmd.client import Client

# Main class
class Static:
    def __init__(self, base_url: str = "https://static.dmmdgm.dev") -> None:
        self.client = Client(base_url)

    # Endpoint handlers
    async def directory(self, path: str = "") -> list[str]:
        return await self.client.request(f"/d/{path}")

    async def file(self, path: str) -> bytes:
        return await self.client.request(f"/f/{path}")
