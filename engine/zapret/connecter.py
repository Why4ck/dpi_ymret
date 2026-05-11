from pathlib import Path
import subprocess
import psutil
import asyncio

dir_now = Path(__file__).parent
process_names = ['winws.exe']

async def kill():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] in process_names:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

async def connect():
    start_file = dir_now / 'zapret' / 'general (ALT3).bat'
    await asyncio.to_thread(subprocess.run, str(start_file), shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

async def run():
    await kill()
    await connect()
