# iiPythonx / dmmd-py

A Python module for interacting with all of DmmD's (soon to be various) APIs.

## Installation

```sh
uv add git@github.com:iiPythonx/dmmd-py
```

## Modules


### iCDN

```py
from dmmd.icdn import iCDN
connection = iCDN()
```

<details>

<summary>Supported Endpoints</summary>

```py
class SortOrder(Enum):
    ASCENDING
    DESCENDING

class SortType(Enum):
    NAME
    TIME
    UUID

type DataModel = {
    data: dict
    mime: str
    name: str
    size: int
    tags: list[str]
    time: datetime
    uuid: str
}

type StoreModel = {
    file_limit:  int
    store_limit: int
    length:      int
    protected:   bool
    size:        int
}

iCDN.file(uuid: str) -> bytes

iCDN.query(uuid: str) -> DataModel

iCDN.search(
    begin?:  int,
    end?:    int,
    count?   int         = 25,
    loose?:  bool        = False,
    name?:   str,
    order?:  SortOrder   = SortOrder.DESCENDING,
    page?:   int         = 0,
    sort?:   SortType    = SortType.TIME,
    tags?:   list[str],
    uuid?:   str
) -> list[str[UUID]]

iCDN.all(
    count?: int = 25
    page?:  int = 0
) -> list[DataModel]

iCDN.list(
    count?: int = 25
    page?:  int = 0
) -> list[str[UUID]]

iCDN.add(
    file:   Path,
    name:   str,
    data?:  dict      = {},
    tags?:  list[str] = [],
    time?:  datetime  = datetime.now(),
    token?: str
) -> DataModel

iCDN.update(
    uuid:   str,
    file?:  Path,
    name?:  str,
    data?:  dict      = {},
    tags?:  list[str] = [],
    time?:  datetime  = datetime.now(),
    token?: str
) -> DataModel

iCDN.remove(
    uuid:   str,
    token?: str
) -> DataModel

iCDN.store() -> StoreModel
```

</details>

<details>

<summary>Exceptions</summary>

- dmmd.exceptions.DmmDException
    - dmmd.exceptions.BadFile
    - dmmd.exceptions.BadJSON
    - dmmd.exceptions.GenericInvalid
        - dmmd.exceptions.InvalidData
        - dmmd.exceptions.InvalidName
        - dmmd.exceptions.InvalidTags
        - dmmd.exceptions.InvalidTime
        - dmmd.exceptions.InvalidToken
        - dmmd.exceptions.InvalidUUID
    - dmmd.exceptions.LargeSource
    - dmmd.exceptions.MissingAsset
    - dmmd.exceptions.MissingContent
    - dmmd.exceptions.UnauthorizedToken
    - dmmd.exceptions.UnsupportedMime

</details>

## Exceptions

- dmmd.exceptions.DmmDException
    - dmmd.exceptions.ServerError
        - Fired when the server replies with an unknown status code.
