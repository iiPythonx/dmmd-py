# Copyright (c) 2025 iiPython

# Modules
import os
import typing
from time import time as take_time
from pathlib import Path
from datetime import datetime

import asyncclick
from humanize import precisedelta

from dmmd.exceptions import DmmDException
from dmmd.icdn import DataModel, SortOrder, SortType, iCDN

# Initialization
def get_cdn() -> iCDN:
    return iCDN(os.environ.get("ICDN_URL", "https://dmmdgm.dev"))

@asyncclick.group(epilog = "Copyright (c) 2025 iiPython")
@asyncclick.option("--url")
def icdn(url: str) -> None:
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
async def query(uuid: str) -> None:
    try:
        full_view(await get_cdn().query(uuid))

    except DmmDException as e:
        print(f"\033[2K\r\033[31mFailed to perform query:\n  > {e}")

@icdn.command()
@asyncclick.option("--begin", type = int, required = False, help = "All content must have an associated time after the specified timestamp.")
@asyncclick.option("--end", type = int, required = False, help = "All content must have an associated time before the specified timestamp.")
@asyncclick.option("--count", type = int, required = False, help = "The number of UUIDs returned per page.")
@asyncclick.option("--loose", type = bool, is_flag = True, default = False, required = False, help = "If true, only require one filter to be true instead of all.")
@asyncclick.option("--order", type = asyncclick.Choice(["asc", "dsc"], case_sensitive = False), default = "dsc", required = False, help = "Sort UUIDs by ascending or descending order.")
@asyncclick.option("--page", type = int, required = False, help = "Page offset.")
@asyncclick.option("--sort", type = asyncclick.Choice(["name", "time", "uuid"], case_sensitive = False), default = "time", required = False, help = "Sorting algorithm to use.")
@asyncclick.option("--tags", type = str, required = False, help = "All content must contain the specified tags, seperated by a comma.")
@asyncclick.option("--uuid", type = str, required = False, help = "Filter by an exact UUID.")
@asyncclick.argument("name", nargs = -1, required = False)
async def search(begin: int, end: int, count: int, loose: bool, order: str, page: int, sort: str, tags: str, uuid: str, name: tuple[str]) -> None:
    for uuid in await get_cdn().search(
        begin, end, count, loose,
        " ".join(name),
        {"ASC": SortOrder.ASCENDING, "DSC": SortOrder.DESCENDING}[order.upper()],
        page,
        {"NAME": SortType.NAME, "TIME": SortType.TIME, "UUID": SortType.UUID}[sort.upper()],
        tags.split(",") if tags is not None else None,
        uuid
    ):
        print(f"\033[32m{uuid}\033[0m")

@icdn.command()
@asyncclick.option("--count", type = int, required = False, default = 25, help = "The number of UUIDs returned per page.")
@asyncclick.option("--page", type = int, required = False, default = 1, help = "Page offset.")
@asyncclick.option("--full", type = bool, is_flag = True, required = False, default = False, help = "Show all packets in the full view.")
async def all(count: int, page: int, full: bool) -> None:
    response = await get_cdn().all(count, page - 1)
    if not response:
        return print("\033[31mNo packets were returned.\033[0m")

    print(f"Showing {len(response)} entries from page {page}:")
    for packet in response:
        if full:
            full_view(packet)
            print()

        else:
            print(f"  * \033[32m{packet.name} ({packet.uuid})\033[0m")

@icdn.command()
@asyncclick.option("--count", type = int, required = False, default = 25, help = "The number of UUIDs returned per page.")
@asyncclick.option("--page", type = int, required = False, default = 1, help = "Page offset.")
@asyncclick.option("--save", type = asyncclick.Path(path_type = Path), required = False, help = "File to save UUIDs to.")
async def list(count: int, page: int, save: typing.Optional[Path] = None) -> None:
    uuids = await get_cdn().list(count, page - 1)
    if not uuids:
        return print("\033[31mNo UUIDs were returned.\033[0m")

    print(f"Showing {len(uuids)} entries from page {page}:")
    print("\n".join(f"  * \033[32m{uuid}\033[0m" for uuid in uuids[:10]))

    if save is not None:
        save.write_text("\n".join(uuids))
        print(f"\nSaved to \033[33m{save}\033[0m.")

async def upload(
    file: Path,
    token: typing.Optional[str] = None,
    time: typing.Optional[int] = None,
    name: typing.Optional[tuple[str]] = None,
    uuid: typing.Optional[str] = None
) -> None:
    if not file.is_file():
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
            "file": file,
            "name": processed_name,
            "data": data,
            "tags": tags,
            "time": datetime.fromtimestamp(time / 1000) if time is not None else datetime.now(),
            "token": token
        } | ({"uuid": uuid} if uuid is not None else {})
        response = await getattr(get_cdn(), "add" if uuid is None else "update")(**kwargs)

        print(
            f"\r\033[32m✓ Upload complete \033[90min \033[36m{round(take_time() - start_time, 1)}s\033[90m. " +
            f"{'New ' if uuid is None else ''}UUID: \033[33m{response.uuid}\033[90m."
        )

    except DmmDException as e:
        print(f"\033[2K\r\033[31mFailed to upload:\n  > {e}")

@icdn.command()
@asyncclick.option("--file", type = asyncclick.Path(path_type = Path, exists = True, dir_okay = False), required = True, help = "File to upload to the iCDN.")
@asyncclick.option("--token", type = str, required = False, help = "Token to use for uploading.")
@asyncclick.option("--time", type = int, required = False, help = "Millisecond based timestamp to use instead of the current time.")
@asyncclick.argument("name", nargs = -1, required = False)
async def add(file: Path, token: typing.Optional[str] = None, time: typing.Optional[int] = None, name: typing.Optional[tuple[str]] = None) -> None:
    await upload(file, token, time, name)

@icdn.command()
@asyncclick.option("--file", type = asyncclick.Path(path_type = Path, exists = True, dir_okay = False), required = True, help = "File to upload to the iCDN.")
@asyncclick.option("--token", type = str, required = False, help = "Token to use for uploading.")
@asyncclick.option("--time", type = int, required = False, help = "Millisecond based timestamp to use instead of the current time.")
@asyncclick.option("--uuid", type = str, required = True, help = "UUID to update.")
@asyncclick.argument("name", nargs = -1, required = False)
async def update(file: Path, uuid: str, token: typing.Optional[str] = None, time: typing.Optional[int] = None, name: typing.Optional[tuple[str]] = None) -> None:
    await upload(file, token, time, name, uuid)

@icdn.command()
@asyncclick.option("--token", type = str, required = False, help = "Token to use for uploading.")
@asyncclick.argument("uuid")
async def remove(uuid: str, token: typing.Optional[str] = None) -> None:
    try:
        await get_cdn().remove(uuid, token)
        print(f"\033[32m✓ Removed \033[33{uuid}\033[32m without issues.")

    except DmmDException as e:
        print(f"\033[2K\r\033[31mFailed to remove:\n  > {e}")
