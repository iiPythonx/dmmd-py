# Copyright (c) 2025 iiPython

import typing
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from dmmd.client import Client

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

type UUID = str

class BuiltCallable:
    def __init__(self, client: Client, endpoint: str, params: dict) -> None:
        self.client, self.endpoint, self.params = client, endpoint, {k :v for k, v in params.items() if v is not None}

    @typing.overload
    async def _perform(self, query: typing.Literal[True]) -> list[DataModel]: ...

    @typing.overload
    async def _perform(self, query: typing.Literal[False]) -> list[UUID]: ...

    async def _perform(self, query: bool) -> list[DataModel] | list[UUID]:
        payload = await self.client.request(self.endpoint, params = self.params | {"query": str(query).lower()})
        return [DataModel(**item) for item in payload] if query else payload

    async def fetch(self) -> list[UUID]:
        return await self._perform(query = False)

    async def query(self) -> list[DataModel]:
        return await self._perform(query = True)
