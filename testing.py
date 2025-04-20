import asyncio
from dmmd.icdn import iCDN
from pathlib import Path

async def main() -> None:
    cdn = iCDN("https://dev.dmmdgm.dev")
    data = await cdn.content("0196514b-4752-7000-bb5a-f036b8b82144")
    print(data.time)

asyncio.run(main())
