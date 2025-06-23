# Copyright (c) 2025 iiPython

import typing
from datetime import datetime

from pydantic import BaseModel, field_validator

class Tag(BaseModel):
    id:   str
    name: str

class Anime(BaseModel):
    begin:   typing.Optional[datetime]    = None
    comment: typing.Optional[str]         = None
    end:     typing.Optional[datetime]    = None
    id:      str
    name:    str
    rating:  typing.Optional[int | float] = None
    tags:    list[str]
    title:   str
    wiki:    typing.Optional[str]         = None

    @field_validator("begin", mode = "before")
    def convert_begin(cls, value: str | None) -> datetime | None:
        return datetime.strptime(value, "%Y-%m-%d") if value is not None else None

    @field_validator("end", mode = "before")
    def convert_end(cls, value: str | None) -> datetime | None:
        return datetime.strptime(value, "%Y-%m-%d") if value is not None else None

class Game(Anime):
    users: list[str]
