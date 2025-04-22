# Copyright (c) 2025 iiPython

# Modules
import json
import typing
from enum import Enum
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from dmmd.client import Client

# Typing
class SortOrder(Enum):
    ASCENDING  = "ascending"
    DESCENDING = "descending"

class SortType(Enum):
    NAME = "name"
    TIME = "time"
    UUID = "uuid"
    SIZE = "size"

class DataModel(BaseModel):
    data: dict
    mime: str
    name: str
    size: int
    tags: list[str]
    time: datetime
    uuid: str

    @field_validator("time", mode = "before")
    def convert_timestamp(cls, value: int) -> datetime:
        return datetime.fromtimestamp(value / 1000)

class StoreModel(BaseModel):
    file_limit:  int = Field(alias = "fileLimit")
    store_limit: int = Field(alias = "storeLimit")
    length:      int
    protected:   bool
    size:        int

# Main class
class iCDN:
    def __init__(self, base_url: str = "https://dmmdgm.dev") -> None:
        self.client = Client(base_url)

    # Endpoint handlers
    async def file(self, uuid: str) -> bytes:
        async with self.client._client.get(f"/file/{uuid}") as response:
            return await response.read()

    async def query(self, uuid: str) -> DataModel:
        return DataModel(**await self.client.request(f"/query/{uuid}"))

    async def search(
        self,
        begin:     typing.Optional[int]       = None,
        end:       typing.Optional[int]       = None,
        minimum:   typing.Optional[int]       = None,
        maximum:   typing.Optional[int]       = None,
        count:     int                        = 25,
        loose:     bool                       = False,
        name:      typing.Optional[str]       = None,
        order:     SortOrder                  = SortOrder.DESCENDING,
        page:      int                        = 0,
        sort:      SortType                   = SortType.TIME,
        tags:      typing.Optional[list[str]] = None,
        uuid:      typing.Optional[str]       = None,
        mime:      typing.Optional[str]       = None,
        extension: typing.Optional[str]       = None
    ) -> list[str]:
        return await self.client.request("/search", params = {
            key: value
            for key, value in {
                "begin": begin, "end": end, "minimum": minimum, "maximum": maximum,
                "count": count, "loose": str(loose).lower(), "name": name, "order": order.value,
                "page": page, "sort": sort.value, "tags": ",".join(tags) if tags else None,
                "uuid": uuid,  "mime": mime, "extension": extension
            }.items() if value is not None
        })

    async def all(self, count: int = 25, page: int = 0) -> list[DataModel]:
        return [
            DataModel(**item) for item in
            await self.client.request("/all", params = {"count": count, "page": page})
        ]

    async def update(
        self,
        uuid:  str,
        file:  typing.Optional[Path]                  = None,
        name:  typing.Optional[str]                   = None,
        data:  typing.Optional[dict[str, typing.Any]] = None,
        tags:  typing.Optional[list[str]]             = None,
        time:  typing.Optional[datetime]              = None,
        token: typing.Optional[str]                   = None
    ) -> DataModel:
        async def process_update(handle = None) -> DataModel:
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
            return DataModel(**response)

        if file is not None:
            with file.open("rb") as handle:
                return await process_update(handle)

        else:
            return await process_update()

    async def remove(self, uuid: str, token: typing.Optional[str] = None) -> DataModel:
        response = await self.client.request("/remove", data = {
            "json": json.dumps({"uuid": uuid} | ({"token": token} if token is not None else {}))
        })
        return DataModel(**response)

    async def list(self, count: int = 25, page: int = 0) -> list[str]:
        return await self.client.request("/list", params = {"count": count, "page": page})

    async def store(self) -> StoreModel:
        return StoreModel(**await self.client.request("/store"))
