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

<summary>CLI</summary>

```sh
icdn query <UUID>
icdn search --begin --end --minimum --maximum --count --loose --order --page --sort --tags --uuid --query NAME
icdn list --count --page --query
icdn add --file --token --time NAME
icdn update --file --token --time --uuid NAME
icdn remove --token <UUID>
icdn details
```

Nearly everything is optional, for more information, run `icdn --help` or check [DmmD's detailed API docs](https://github.com/DmmDGM/dmmd-icdn).

</details>

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
    file_limit:   int
    store_limit:  int
    store_length: int
    store_size:   int
    protected:    bool
}

async iCDN.file(uuid: str) -> bytes

async iCDN.query(uuid: str) -> DataModel

async iCDN.add(
    file:   Path,
    name:   str,
    data?:  dict      = {},
    tags?:  list[str] = [],
    time?:  datetime  = datetime.now(),
    token?: str
) -> DataModel

async iCDN.update(
    uuid:   str,
    file?:  Path,
    name?:  str,
    data?:  dict      = {},
    tags?:  list[str] = [],
    time?:  datetime  = datetime.now(),
    token?: str
) -> DataModel

async iCDN.remove(
    uuid:   str,
    token?: str
) -> DataModel

async iCDN.store() -> StoreModel

iCDN.search(
    begin?:   int,
    end?:     int,
    minimum?: int,
    maximum?: int
    count?    int         = 25,
    loose?:   bool        = False,
    name?:    str,
    order?:   SortOrder   = SortOrder.DESCENDING,
    page?:    int         = 0,
    sort?:    SortType    = SortType.TIME,
    tags?:    list[str],
    uuid?:    str
} -> BuiltCallable

iCDN.list(
    count?: int  = 25
    page?:  int  = 0
) -> BuiltCallable

async BuiltCallable.fetch() -> list[UUID]
async BuiltCallable.query() -> list[DataModel]
```

All endpoints that support querying must be called first with your arguments, and then awaited with any additional options. An example of this is as follows:

```py
endpoint = iCDN.search("bocchi the rock")
await endpoint.query()  # Returns a list of BaseModels
await endpoint.fetch()  # Returns a list of UUIDs
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

### Static

```py
from dmmd.static import Static
connection = Static()
```

<details>

<summary>Supported Endpoints</summary>

```py
async Static.directory(path?: str = "") -> list[str]
async Static.file(path: str) -> bytes
```

</details>

<details>

<summary>Exceptions</summary>

- dmmd.exceptions.DmmDException
    - dmmd.exceptions.OutOfBoundsFile
    - dmmd.exceptions.UnknownEndpoint
    - dmmd.exceptions.UnknownDirectory
    - dmmd.exceptions.UnknownFile

</details>

## Exceptions

- dmmd.exceptions.DmmDException
    - dmmd.exceptions.ServerError
        - Fired when the server replies with an unknown status code.
    - dmmd.exceptions.UnauthorizedToken
