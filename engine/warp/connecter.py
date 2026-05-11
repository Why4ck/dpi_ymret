import subprocess
import os
import sys
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__)) # dirs
parent_dir = os.path.dirname(current_dir) # engine dir
root_dir = os.path.dirname(parent_dir) # project dir
sys.path.append(root_dir)

from logger import setup_logger
logger = setup_logger()

async def connect():
    connection = subprocess.run(['warp-cli', 'connect'], capture_output=True, )

async def disconnect():
    disconnection = subprocess.run(['warp-cli', 'disonnect'], capture_output=True, )

async def __status():
    res = await asyncio.to_thread(
        subprocess.run, 
        ['warp-cli', 'status'], 
        capture_output=True, 
        text=True
    )
    
    txt = res.stdout + res.stderr
    
    d = {
        k.strip(): v.strip() 
        for line in txt.strip().splitlines() 
        if ':' in line 
        for k, v in [line.split(':', 1)]
    }
    
    return d

async def checker():
    data = await __status()
    if data['Status update'] == 'Connected':
        return True
    else:
        return False

async def main():
    await disconnect()
    await connect()
    
    data = await checker()
    return data