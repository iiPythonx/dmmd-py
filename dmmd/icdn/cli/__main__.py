# Copyright (c) 2025 iiPython

# Modules
import os
import typing
import mimetypes
from time import time as take_time
from pathlib import Path
from datetime import datetime

import asyncclick
from humanize import precisedelta, naturalsize

from dmmd.exceptions import DmmDException
from dmmd.icdn import DataModel, SortOrder, SortType, iCDN
from dmmd.icdn.cli.parameters import attach, search_params, generic_add

# Initialization
def get_cdn() -> iCDN:
    return iCDN(os.environ.get("ICDN_URL", "https://dmmdgm.dev"))

@asyncclick.group(epilog = "Copyright (c) 2025 iiPython")
def icdn() -> None:
    """A Python-based CLI for DmmD's iCDN.

    \b
    Source code       : https://github.com/iiPythonx/dmmd-py
    API documentation : https://github.com/DmmDGM/dmmd-icdn
    """
    return

# Generic UI
def field(title: str, value: str) -> None:
    print(f"\n  \033[34m{title}:\n    \033[33m{value}")

def full_view(response: DataModel) -> None:
    print(f"\033[90m* \033[36m{response.name}\033[0m \033[90m(\033[33m{response.uuid}\033[0m\033[90m, {response.mime})")
    field("File tags", ", ".join(f"\033[32m{tag}\033[90m" for tag in response.tags))
    field("Added at", response.time.strftime("%D %I:%M:%S %p (Local)"))
    print(f"    ({precisedelta(datetime.now() - response.time, format = "%.0f")} ago)")

    # Show data (if we have any)
    if response.data:
        print("\n  \033[34mAdditional data:")
        for k, v in response.data.items():
            print(f"    \033[34m{k}\033[90m: \033[32m{v}")

# Commands
@icdn.command()
@asyncclick.argument("uuid")
@asyncclick.argument("file", type = asyncclick.Path(dir_okay = False, path_type = Path), required = False)
async def download(uuid: str, file: typing.Optional[Path] = None) -> None:
    try:
        cdn = get_cdn()

        # Calculate output file
        data = await cdn.query(uuid)
        path = file or Path(f"{data.name}{mimetypes.guess_extension(data.mime)}")

        path.write_bytes(await cdn.file(uuid))
        print(f"\033[32m✓ Download complete as \033[34m{path.name}\033[32m.\033[0m")

    except DmmDException as e:
        print(f"\033[2K\r\033[31mFailed to download:\n  > {e}")

@icdn.command()
@asyncclick.argument("uuid")
async def query(uuid: str) -> None:
    try:
        full_view(await get_cdn().query(uuid))

    except DmmDException as e:
        print(f"\033[2K\r\033[31mFailed to perform query:\n  > {e}")

@icdn.command()
@asyncclick.argument("name", nargs = -1, required = False)
async def search(name: tuple[str], **kwargs) -> None:
    response = await getattr(get_cdn(), "search_query" if kwargs.get("query") else "search")(kwargs | {
        "name": " ".join(name) if name else None,
        "order": {"ASC": SortOrder.ASCENDING, "DSC": SortOrder.DESCENDING}[kwargs["order"].upper()],
        "sort": {"NAME": SortType.NAME, "TIME": SortType.TIME, "UUID": SortType.UUID, "SIZE": SortType.SIZE}[kwargs["sort"].upper()],
        "tags": kwargs["tags"].split(",") if kwargs["tags"] is not None else None
    })  # type: ignore
    if kwargs.get("query"):
        [print(f"* \033[32m{uuid}\033[0m") for uuid in response]

    else:
        [full_view(summary) for summary in response]

attach(search_params, search)

@icdn.command()
@asyncclick.option("--count", type = int, required = False, default = 25, help = "The number of UUIDs returned per page.")
@asyncclick.option("--page", type = int, required = False, default = 1, help = "Page offset.")
@asyncclick.option("--query", type = bool, is_flag = True, required = False, default = False, help = "Show entire summaries instead of just UUIDs.")
async def list(count: int, page: int, query: bool) -> None:
    response = await getattr(get_cdn(), "list_query" if query else "list")(count, page - 1)
    if not response:
        return print("\033[31mNo items were returned.\033[0m")

    print(f"Showing {len(response)} items from page {page}:")
    if not query:
        print("\n".join(f"  * \033[32m{uuid}\033[0m" for uuid in response))

    else:
        [full_view(summary) for summary in response]

async def upload(
    file: typing.Optional[Path] = None,
    token: typing.Optional[str] = None,
    time: typing.Optional[int] = None,
    name: typing.Optional[tuple[str]] = None,
    uuid: typing.Optional[str] = None
) -> None:
    if file and not file.is_file():
        return print("\033[31m--file must be a valid file that \033[4mactually exists\033[24m.")

    processed_name = " ".join(name) if name else input("\033[36mName: \033[0m")

    print("\033[36mPlease attach any tags now \033[90m(seperated by commas, space optional)\033[36m:")
    tags = [tag.strip() for tag in input("\033[90m  > \033[0m").split(",") if tag.strip()]
    print(f"\033[1A\r  \033[90m> {(', '.join(f'\033[32m{tag}\033[90m' for tag in tags)) if tags else '\033[32m✓ None'}")

    print("\n\033[36mAttach any \033[33m*additional*\033[36m data now \033[90m(optional, leave anything blank to continue)\033[36m:")
    data = {}
    while True:
        key = input("\033[34m  Name: \033[0m")
        if not key.strip():
            break

        print(f"\033[1A\r  \033[34mName: \033[33m{key} \033[32m✓\033[0m \033[90m| ", end = "", flush = True)
        value = input("\033[34mData: \033[0m")
        if not value.strip():
            break

        data[key] = value
        print(f"\033[1A\r  \033[34mName: \033[33m{key} \033[90m| \033[34mData: \033[33m{value} \033[32m✓\033[0m")

    print("\033[1A\033[2K", end = "", flush = True)  # Erase last line of data fetching
    print("" if data else "  \033[90m> \033[32m✓ None", end = "\n\n")

    print("\033[33mUpload in progress...", end = "", flush = True)

    try:
        start_time = take_time()

        # Create kwargs
        kwargs = {
            "name": processed_name,
            "data": data,
            "tags": tags,
            "time": datetime.fromtimestamp(time / 1000) if time is not None else datetime.now(),
            "token": token
        } | ({"uuid": uuid} if uuid is not None else {}) | ({"file": file} if file is not None else {})
        response = await getattr(get_cdn(), "add" if uuid is None else "update")(**kwargs)

        print(
            f"\r\033[32m✓ Upload complete \033[90min \033[36m{round(take_time() - start_time, 1)}s\033[90m. " +
            f"{'New ' if uuid is None else ''}UUID: \033[33m{response.uuids[0]}\033[90m."
        )

    except DmmDException as e:
        print(f"\033[2K\r\033[31mFailed to upload:\n  > {e}")

@icdn.command()
@asyncclick.option("--file", type = asyncclick.Path(path_type = Path, exists = True, dir_okay = False), required = True, help = "File to upload to the iCDN.")
@asyncclick.argument("name", nargs = -1, required = False)
async def add(file: Path, token: typing.Optional[str] = None, time: typing.Optional[int] = None, name: typing.Optional[tuple[str]] = None) -> None:
    await upload(file, token, time, name)

attach(generic_add, add)

@icdn.command()
@asyncclick.option("--file", type = asyncclick.Path(path_type = Path, exists = True, dir_okay = False), required = False, help = "File to upload to the iCDN.")
@asyncclick.option("--uuid", type = str, required = True, help = "UUID to update.")
@asyncclick.argument("name", nargs = -1, required = False)
async def update(
    uuid: str,
    file: typing.Optional[Path] = None,
    token: typing.Optional[str] = None,
    time: typing.Optional[int] = None,
    name: typing.Optional[tuple[str]] = None
) -> None:
    await upload(file, token, time, name, uuid)

attach(generic_add, update)

@icdn.command()
@asyncclick.option("--token", type = str, required = False, help = "Token to use for uploading.")
@asyncclick.argument("uuid")
async def remove(uuid: str, token: typing.Optional[str] = None) -> None:
    try:
        await get_cdn().remove(uuid, token)
        print(f"\033[32m✓ Removed \033[33{uuid}\033[32m without issues.")

    except DmmDException as e:
        print(f"\033[2K\r\033[31mFailed to remove:\n  > {e}")

@icdn.command()
async def details() -> None:
    store = await get_cdn().details()
    print(f"\033[90mCurrent usage: \033[36m{naturalsize(store.store_size)} \033[90m/ \033[36m{naturalsize(store.store_limit)} \033[90m(\033[36m{round((store.store_size / store.store_limit) * 100, 1)}%\033[90m)")
    print(f"\033[90mFile size limit: \033[36m{naturalsize(store.file_limit)}\033[90m, Current files: \033[36m{store.store_length}\033[90m, Protected: {'\033[31myes' if store.protected else '\033[32mno'}")
