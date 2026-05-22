import connect
import asyncio
import win32con
import win32api
import atexit
import killall
from engine import main_connector as connector
from pathlib import Path
from elevate import elevate
from colorama import init, Fore, Style
import sys
import time
import subprocess
import os
import installer  # Импортируем установщик напрямую

init()

text = """
████  ████  ███    █   █ █   █ ████  █████ █████   
█░░░█ █░░░█  █░░    █ █ ░██ ██░█░░░█ █░░░░░ ░█░░░  
█░░░█░████░░ █░░░    █ ░ █░█ █░████░░████░░░ █░░░░ 
█░░ █░█░░░░ ░█░░     █░ ░█░░░█░█░░█░ █░░░░   █░░   
████ ░█░░░░░███░     █░░ █░░ █░█░░░█░█████░  █░░   
 ░░░░ ░░░    ░░░      ░░  ░░  ░░░░  ░ ░░░░░   ░░   
  ░░░░  ░     ░░░      ░   ░   ░ ░   ░ ░░░░░   ░  

Autor - Why4ck (https://github.com/why4ck)
dpi ymret source - https://github.com/why4ck/dpi_ymret
Version - 0.1
"""

menu_text = '''
[0] Exit                           [3] Connect only Goodbyedpi                [7] Update and debug
[1] Connect Auto config (best)     [4] Connect only Zapret                    
[2] Disconnect                     [5] Connect only Zapret2                   
                                   [6] Connect only warp (NOT FOR RUSSIA)
'''

try:
    asyncio.run(killall.run())
except Exception:
    pass

def do_cleanup():
    try:
        processes_to_kill = ["goodbyedpi.exe", "zapret.exe", "warp.exe", "winws.exe"] 
        for proc in processes_to_kill:
            subprocess.call(f"taskkill /F /IM {proc} >nul 2>&1", shell=True)
    except Exception:
        pass

atexit.register(do_cleanup)

def win_handler(dwCtrlType):
    if dwCtrlType == win32con.CTRL_CLOSE_EVENT:
        do_cleanup()
        time.sleep(2)
        return True
    return False

win32api.SetConsoleCtrlHandler(win_handler, True)

async def main():
    print(Fore.RED, text, Style.RESET_ALL, sep='')
    print(Fore.BLUE, menu_text, Style.RESET_ALL, sep='')
    
    while True:
        try:
            user_input = input(': ')
            
            if user_input.lower() in ('q', 'exit', ''):
                break
                
            data = int(user_input)
            
            if data == 0:
                break

        except ValueError:
            print("Input a number")
            continue

        # Обработка пункта 7 (Обновление) отдельно, чтобы избежать сложностей со словарем
        if data == 7:
            print("Starting update process...")
            try:
                # Запускаем установку в_hard режиме
                success = await installer.main()
                if success:
                    print("Update successful. Restarting menu...")
                    # Очищаем экран и перезапускаем цикл меню
                    os.system('cls')
                    continue 
                else:
                    print("Update failed.")
            except Exception as e:
                print(f"Update error: {e}")
            continue

        input_enter_does = {
            1: connect.goodbyedpi,
            2: killall.run,
            3: connector.start_goodbyedpi,
            4: connector.start_zapret,
            5: connector.start_zapret2,
            6: connector.start_warp,
        }

        if data not in input_enter_does:
            print('Input other number')
            continue

        try:
            result = await input_enter_does[data]()
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}")