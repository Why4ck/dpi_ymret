import subprocess
import psutil
import asyncio

async def kill_process(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except Exception:
                pass
            

async def run():
    await kill_process('winws2.exe')
    await kill_process('winws.exe')
    await kill_process('goodbyedpi.exe')

    async def kill_warp():
        subprocess.run(['warp-cli', 'disconnect'], capture_output=True)
    
    await kill_warp()

if __name__ == "__main__":
    asyncio.run(run())