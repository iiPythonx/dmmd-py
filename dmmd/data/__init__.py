# Copyright (c) 2025 iiPython

# Modules
from dmmd.client import Client
from dmmd.data._typing import Anime, Game, Tag

# Main class
class Data:
    def __init__(self, base_url: str = "https://dmmdgm.dev") -> None:
        self.client = Client(base_url)

    # Endpoint handlersanime
    async def tags(self) -> list[Tag]:
        return [Tag(**tag) for tag in await self.client.request("/api/data/tags")]

    async def anime(self) -> list[Anime]:
        return [Anime(**tag) for tag in await self.client.request("/api/data/anime")]

    async def games(self) -> list[Game]:
        return [Game(**tag) for tag in await self.client.request("/api/data/games")]
