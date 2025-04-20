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
connection = iCDN("https://random.dmmdgm.dev")
```

#### Supported endpoints

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
    name: str
    tags: list[str]
    time: datetime
    uuid: str
}

iCDN.content(uuid: str) -> bytes

iCDN.data(uuid: str) -> DataModel

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
) -> bool[Success]

iCDN.update(
    uuid:   str,
    file?:  Path,
    name?:  str,
    data?:  dict      = {},
    tags?:  list[str] = [],
    time?:  datetime  = datetime.now(),
    token?: str
) -> bool[Success]

iCDN.remove(
    uuid:   str,
    token?: str
) -> bool[Success]
```

#### Exceptions

None specific to iCDN at this time.

## Exceptions

- dmmd.exceptions.DmmDException
    - dmmd.exceptions.BadRequest
        - Fired when the server replies with a 400, also contains the response text.
    - dmmd.exceptions.NotFound
        - Fired when a 404 is received, also contains the endpoint URL.
    - dmmd.exceptions.ServerError
        - Fired when the server replies with an unknown status code.
