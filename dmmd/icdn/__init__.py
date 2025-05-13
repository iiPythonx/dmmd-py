# Copyright (c) 2025 iiPython

# Modules
import json
import typing
from pathlib import Path
from datetime import datetime

from dmmd.client import Client
from dmmd.icdn._typing import BuiltCallable, DataModel, SortOrder, SortType, StoreModel

# Main class
class iCDN:
    def __init__(self, base_url: str = "https://dmmdgm.dev") -> None:
        self.client = Client(base_url)

    # Endpoint handlers
    async def file(self, uuid: str) -> bytes:
        return await self.client.request(f"/file/{uuid}")

    async def query(self, uuid: str) -> DataModel:
        return DataModel(**await self.client.request(f"/query/{uuid}"))

    def search(
        self,
        name:      typing.Optional[str]       = None                ,
        begin:     typing.Optional[int]       = None                ,
        end:       typing.Optional[int]       = None                ,
        maximum:   typing.Optional[int]       = None                ,
        minimum:   typing.Optional[int]       = None                ,
        uuid:      typing.Optional[str]       = None                ,
        mime:      typing.Optional[str]       = None                ,
        extension: typing.Optional[str]       = None                ,
        count:     typing.Optional[int]       = 25                  ,
        loose:     typing.Optional[bool]      = False               ,
        page:      typing.Optional[int]       = 0                   ,
        tags:      typing.Optional[list[str]] = []                  ,
        order:     SortOrder                  = SortOrder.DESCENDING,
        sort:      SortType                   = SortType.TIME       ,
    ) -> BuiltCallable:
        return BuiltCallable(self.client, "/search", {
            "begin":     begin,
            "end":       end,
            "maximum":   maximum,
            "minimum":   minimum,
            "name":      name,
            "uuid":      uuid,
            "mime":      mime,
            "extension": extension,
            "count":     count,
            "loose":     str(loose).lower(),
            "order":     order.value,
            "page":      page,
            "sort":      sort.value,
            "tags":      ",".join(tags) if tags else None
        })

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
    def list(self, count: int = 25, page: int = 0) -> BuiltCallable:
        return BuiltCallable(
            self.client,
            "/list",
            {
                "count": count,
                "page": page
            }
        )

    async def details(self) -> StoreModel:
        return StoreModel(**await self.client.request("/details"))
