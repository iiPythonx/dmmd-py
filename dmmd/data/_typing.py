# Copyright (c) 2025 iiPython

import typing
from pydantic import BaseModel

class Tag(BaseModel):
    id:   str
    name: str

class Anime(BaseModel):
    begin:   typing.Optional[str]         = None
    comment: typing.Optional[str]         = None
    end:     typing.Optional[str]         = None
    id:      str
    name:    str
    rating:  typing.Optional[int | float] = None
    tags:    list[str]
    title:   str
    wiki:    typing.Optional[str]         = None

class Game(Anime):
    users: list[str]
