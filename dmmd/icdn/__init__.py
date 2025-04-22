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
    file_limit:   int = Field(alias = "fileLimit")
    store_limit:  int = Field(alias = "storeLimit")
    store_length: int = Field(alias = "storeLength")
    store_size:   int = Field(alias = "storeSize")
    protected:    bool

class SearchParams(typing.TypedDict, total = False):
    begin:     int
    end:       int
    minimum:   int
    maximum:   int
    count:     int
    loose:     bool
    name:      str
    order:     SortOrder
    page:      int
    sort:      SortType
    tags:      list[str]
    uuid:      str
    mime:      str
    extension: str

# Main class
class iCDN:
    def __init__(self, base_url: str = "https://dmmdgm.dev") -> None:
        self.client = Client(base_url)

    @staticmethod
    def _sanitize(params: SearchParams) -> dict:
        return {k: v for k, v in (params | {
            "count": params.get("count", 25),
            "loose": str(params.get("loose", False)).lower(),
            "order": params.get("order", SortOrder.DESCENDING).value,
            "tags":  ",".join(params.get("tags", [])) if params.get("tags") else None,
            "sort": params.get("sort", SortType.TIME).value,
            "page": params.get("page", 0)
        }).items() if v is not None}

    # Endpoint handlers
    async def file(self, uuid: str) -> bytes:
        async with self.client._client.get(f"/file/{uuid}") as response:
            return await response.read()

    async def query(self, uuid: str) -> DataModel:
        return DataModel(**await self.client.request(f"/query/{uuid}"))

    async def search(self, params: SearchParams) -> list[str]:
        return await self.client.request("/search", params = self._sanitize(params) | {"query": "false"})

    async def search_query(self, params: SearchParams) -> list[DataModel]:
        return [DataModel(**item) for item in await self.client.request("/search", params = self._sanitize(params) | {"query": "true"})]

    async def add(
        self,
        file:  Path,
        name:  str,
        data:  dict[str, typing.Any]     = {},
        tags:  list[str]                 = [],
        time:  typing.Optional[datetime] = None,
        token: typing.Optional[str]      = None
     ) -> DataModel:
        with file.open("rb") as handle:
            return DataModel(**await self.client.request("/add", data = {
                "file": handle,
                "json": json.dumps({
                    "data": data,
                    "name": name,
                    "tags": tags,
                    "time": round((time or datetime.now()).timestamp() * 1000)
                } | ({"token": token} if token is not None else {}))
            }))

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
            return DataModel(**await self.client.request("/update", data = {
                "json": json.dumps({
                    key: value for key, value in {
                        "uuid": uuid,
                        "data": data,
                        "name": name,
                        "tags": tags,
                        "time": round(time.timestamp() * 1000) if time else None
                    }.items() if value is not None
                } | ({"token": token} if token is not None else {}))
            } | ({"file": handle} if handle else {})))

        if file is not None:
            with file.open("rb") as handle:
                return await process_update(handle)

        else:
            return await process_update()

    async def remove(self, uuid: str, token: typing.Optional[str] = None) -> DataModel:
        return DataModel(**await self.client.request("/remove", data = {
            "json": json.dumps({"uuid": uuid} | ({"token": token} if token is not None else {}))
        }))

    # Handle listing
    async def list_query(self, count: int = 25, page: int = 0) -> list[DataModel]:
        return [DataModel(**item) for item in await self.client.request("/list", params = {"count": count, "page": page, "query": "true"})]

    async def list(self, count: int = 25, page: int = 0) -> list[str]:
        return await self.client.request("/list", params = {"count": count, "page": page, "query": "false"})

    async def details(self) -> StoreModel:
        return StoreModel(**await self.client.request("/details"))
