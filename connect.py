import asyncio
from engine import main_connector as connector
import killall
asyncio.run(killall.run())


async def goodbyedpi():
    await connector.start_goodbyedpi()
    await asyncio.sleep(3)
    await connector.start_warp()

async def zapret():
    await asyncio.gather(
        connector.start_zapret(), 
        connector.start_warp()
    )

async def zapret2():
    await asyncio.gather(
        connector.start_zapret2(), 
        connector.start_warp()
    )

if __name__ == "__main__":
    asyncio.run(goodbyedpi()) # Run the event loop