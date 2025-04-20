# Copyright (c) 2025 iiPython

# Modules
import json
import typing
from enum import Enum
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel, field_validator

from dmmd.client import Client

# Typing
class SortOrder(Enum):
    ASCENDING  = "ascending"
    DESCENDING = "descending"

class SortType(Enum):
    NAME = "name"
    TIME = "time"
    UUID = "uuid"

class DataModel(BaseModel):
    data: dict
    name: str
    tags: list[str]
    time: datetime
    uuid: str

    @field_validator("time", mode = "before")
    def convert_timestamp(cls, value: int) -> datetime:
        return datetime.fromtimestamp(value / 1000)

# Main class
class iCDN:
    def __init__(self, base_url: str = "https://dmmdgm.dev") -> None:
        self.client = Client(base_url)

    # Endpoint handlers
    async def data(self, uuid: str) -> DataModel:
        return DataModel(**await self.client.json(f"/data/{uuid}"))

    async def search(
        self,
        begin: typing.Optional[int]       = None,
        end:   typing.Optional[int]       = None,
        count: int                        = 25,
        loose: bool                       = False,
        name:  typing.Optional[str]       = None,
        order: SortOrder                  = SortOrder.DESCENDING,
        page:  int                        = 0,
        sort:  SortType                   = SortType.TIME,
        tags:  typing.Optional[list[str]] = None,
        uuid:  typing.Optional[str]       = None
    ) -> list[str]:
        return await self.client.json("/search", params = {
            key: value
            for key, value in {
                "begin": begin, "end": end, "count": count, "loose": str(loose).lower(),
                "name": name, "order": order.value, "page": page, "sort": sort.value,
                "tags": ",".join(tags) if tags else None, "uuid": uuid
            }.items() if value is not None
        })

    async def all(self, count: int = 25, page: int = 0) -> list[DataModel]:
        return [
            DataModel(**item) for item in
            await self.client.json("/all", params = {"count": count, "page": page})
        ]

    async def add(
        self,
        file:  Path,
        name:  str,
        data:  dict[str, typing.Any]     = {},
        tags:  list[str]                 = [],
        time:  typing.Optional[datetime] = None,
        token: typing.Optional[str]      = None
    ) -> bool:
        with file.open("rb") as handle:
            response = await self.client.request("/add", data = {
                "file": handle,
                "json": json.dumps({
                    "data": data,
                    "name": name,
                    "tags": tags,
                    "time": round((time or datetime.now()).timestamp() * 1000),
                } | ({"token": token} if token is not None else {}))
            })
            return response == b"OK"

    async def update(
        self,
        uuid:  str,
        file:  typing.Optional[Path]                  = None,
        name:  typing.Optional[str]                   = None,
        data:  typing.Optional[dict[str, typing.Any]] = None,
        tags:  typing.Optional[list[str]]             = None,
        time:  typing.Optional[datetime]              = None,
        token: typing.Optional[str]                   = None
    ) -> bool:
        async def process_update(handle = None) -> bool:
            response = await self.client.request("/update", data = {
                "json": json.dumps({
                    key: value for key, value in {
                        "uuid": uuid,
                        "data": data,
                        "name": name,
                        "tags": tags,
                        "time": round(time.timestamp() * 1000) if time else None
                    }.items() if value is not None
                } | ({"token": token} if token is not None else {}))
            } | ({"file": handle} if handle else {}))
            return response == b"OK"

        if file is not None:
            with file.open("rb") as handle:
                return await process_update(handle)

        else:
            return await process_update()

    async def list(self, count: int = 25, page: int = 0) -> list[str]:
        return await self.client.json("/list", params = {"count": count, "page": page})
