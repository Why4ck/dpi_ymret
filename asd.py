from downloader import wiresock
import asyncio
from elevate import elevate
elevate()
asyncio.run(wiresock())