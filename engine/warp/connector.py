import subprocess # System command execution
import os # OS path operations
import sys # System parameters
import asyncio # Async support
import time # Time functions
from pathlib import Path # Path handling
from elevate import elevate
elevate() # Admin rules

try: # Colorama import with fallback
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore: GREEN = ''; RED = ''
    class Style: RESET_ALL = ''

current_dir = os.path.dirname(os.path.abspath(__file__)) # Current script dir
parent_dir = os.path.dirname(current_dir) # Parent dir
root_dir = os.path.dirname(parent_dir) # Root project dir
sys.path.append(root_dir) # Add root to path

from logger import setup_logger # Custom logger import
logger = setup_logger() # Logger initialization

async def check_warp_installed(): # Check if WARP CLI exists
    try:
        warp_check = await asyncio.to_thread( # Offload blocking call to thread
            subprocess.check_output,
            ["warp-cli", "-V"],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5
        )
        if "warp-cli" in warp_check:
            return True
    except FileNotFoundError:
        return False
    except Exception:
        return False

async def warp_register_account(): # Register WARP account with retry logic
    try:
        show = await asyncio.to_thread( # Offload blocking call
            subprocess.check_output,
            ['warp-cli', 'registration', 'show'], 
            stderr=subprocess.STDOUT,
            text=True
        )
    except subprocess.CalledProcessError as e:
        show = e.output.decode('utf-8', errors='ignore') if isinstance(e.output, bytes) else e.output
    
    if "Error" in show:
        new_reg = await asyncio.to_thread(
            subprocess.run,
            ['warp-cli', 'registration', 'new'],
            capture_output=True,
            text=True
        )
        
        reg_output = new_reg.stdout + new_reg.stderr
        
        if "Success" in reg_output:
            return True
        
        elif "timeout" in reg_output.lower() or "IPC call hit a timeout" in reg_output:
            await asyncio.to_thread( # Kill hanging process
                subprocess.run, 
                ['taskkill', '/f', '/im', 'Cloudflare WARP.exe'], 
                capture_output=True
            )
            
            await asyncio.to_thread( # Delete corrupted registration
                subprocess.run, 
                ['warp-cli', 'registration', 'delete'],
                capture_output=True
            )
            
            retry = await asyncio.to_thread( # Retry registration
                subprocess.run,
                ['warp-cli', 'registration', 'new'],
                capture_output=True,
                text=True
            )
            
            if "Success" in (retry.stdout + retry.stderr):
                return True
            else:
                return False
        else:
            return False
    else:
        return True

async def ensure_warp_ready(): # Verify installation and account status
    is_installed = await check_warp_installed()
    if not is_installed:
        return False
    
    show = await asyncio.to_thread(
        subprocess.run,
        ['warp-cli', 'registration', 'show'],
        capture_output=True, 
        text=True
    )
    
    output = show.stdout + show.stderr
    
    if "Account type" in output:
        return True
    else:
        return await warp_register_account()

async def connect(): # Connect to WARP
    await asyncio.to_thread(
        subprocess.run, 
        ['warp-cli', 'connect'], 
        capture_output=True, 
        text=True
    )

async def disconnect(): # Disconnect from WARP
    await asyncio.to_thread(
        subprocess.run, 
        ['warp-cli', 'disconnect'], # Fixed typo from 'disonnect'
        capture_output=True, 
        text=True
    )

async def __status(): # Parse WARP status output
    res = await asyncio.to_thread(
        subprocess.run, 
        ['warp-cli', 'status'], 
        capture_output=True, 
        text=True
    )
    
    txt = res.stdout + res.stderr
    
    d = {}
    for line in txt.strip().splitlines():
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                k, v = parts
                d[k.strip()] = v.strip()
    
    return d

async def checker(): # Check if connected
    try:
        data = await __status()
        status_val = data.get('Status update') or data.get('Status')
        return status_val == 'Connected'
    except Exception:
        return False

async def run(): # Main execution flow
    
    async def ensure_service_running(): # Start WARP daemon if stopped
        await asyncio.to_thread(
            subprocess.run,
            ['net', 'start', 'CloudflareWARP'],
            capture_output=True
        )
        await asyncio.sleep(2) # Wait for service init
    
    await ensure_service_running()
    
    ready = await ensure_warp_ready() # Ensure WARP is installed and registered
    if not ready:
        return False

    await disconnect()
    await connect()
    
    await asyncio.sleep(3) # Wait for connection establishment
    
    is_connected = await checker()
    return is_connected