import installer
import menu
import asyncio
import os
import sys
from elevate import elevate

elevate()

STATUS_FILE = 'status.dat'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REQUIRED_FILES = [
    os.path.join(BASE_DIR, "engine", "goodbyedpi", "goodbyedpi", "1_russia_blacklist.cmd"),
    os.path.join(BASE_DIR, "engine", "zapret", "zapret", "general (ALT3).bat"),
    os.path.join(BASE_DIR, "engine", "zapret2", "zapret2", "zapret-winws", "winws2.exe")
]

def check_files():
    for f_path in REQUIRED_FILES:
        if not os.path.exists(f_path):
            return False
    return True

def check_status():
    if not os.path.exists(STATUS_FILE):
        return False
    try:
        with open(STATUS_FILE, 'r') as f:
            return f.read().strip() == 'True'
    except:
        return False

def set_status(value: bool):
    with open(STATUS_FILE, 'w') as f:
        f.write(str(value))

async def main(hard: bool = False):
    need_install = False

    if hard:
        print("Hard install mode: forcing installation...")
        need_install = True
    else:
        status_ok = check_status()
        files_ok = check_files()
        
        if not status_ok or not files_ok:
            need_install = True
        else:
            print("System is ready. Skipping installation.")

    if need_install:
        print("Starting installation...")
        try:
            await installer.main()
            
            set_status(True)
            print("Installation completed.")
            
        except Exception as e:
            set_status(False)
            print(f"Installation error: {e}")
            return
            
    print("Starting menu...")
    await menu.main()

if __name__ == "__main__":
    asyncio.run(main())

