import asyncio
from logger import setup_logger
import aiofiles
import downloader
from pathlib import Path
from colorama import init, Fore, Style

logger = setup_logger()

zp2_bat = r"""@echo off
chcp 65001 >nul
cd /d "%~dp0"

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Запусти от имени Администратора!
    pause
    exit /b 1
)

taskkill /F /IM winws2.exe /T >nul 2>&1
timeout /t 1 /nobreak >nul

echo [WinWS2] Starting zapret2
echo.

winws2.exe ^
--wf-tcp-out=80,443 ^
--wf-tcp-in=80,443 ^
--wf-udp-out=443 ^
--wf-udp-in=443 ^
--lua-init=@lua\zapret-lib.lua ^
--lua-init=@lua\zapret-antidpi.lua ^
--filter-tcp=80 --filter-l7=http ^
  --out-range=-d10 ^
  --payload=http_req ^
  --lua-desync=fake:blob=fake_default_http:ip_autottl=-2,3-20:ip6_autottl=-2,3-20:tcp_md5 ^
  --lua-desync=multisplit:pos=1:seqovl=5:seqovl_pattern=0x1603030000 ^
  --new ^
--filter-tcp=443 --filter-l7=tls ^
  --out-range=-d10 ^
  --payload=tls_client_hello ^
  --lua-desync=fake:blob=fake_default_tls:tcp_md5:repeats=11:tls_mod=rnd,rndsni,dupsid,sni=www.google.com ^
  --lua-desync=fakedsplit:pos=method+2:ip_autottl=-2,3-20:ip6_autottl=-2,3-20:tcp_md5 ^
  --new ^
--filter-udp=443 --filter-l7=quic ^
  --out-range=-d10 ^
  --payload=quic_initial ^
  --lua-desync=fake:blob=fake_default_quic:repeats=11 ^
  --new ^
--filter-tcp=443 --filter-l7=unknown ^
  --out-range=a ^
  --payload=unknown ^
  --lua-desync=fake:blob=fake_default_tls:repeats=6:ip_autottl=-2,3-20 ^
  --lua-desync=fakedsplit:pos=1:ip_autottl=-2,3-20

echo.
echo WinWS2 остановлен.
pause"""


async def main():
    print(f"more details in LOGs: {Path(downloader.dir_now / 'app.log')}")
    print(Fore.RED, "Start downloading: goodbyedpi, zapret, zapret", Style.RESET_ALL, sep='')
    await downloader.obfs()
    print(Fore.RED, "End downloading: goodbyedpi, zapret, zapret", Style.RESET_ALL, sep='')
    
    
    # print(Fore.RED, "Start downloading network tools", Style.RESET_ALL, sep='')
    # await downloader.telemetry()
    # print(Fore.RED, "End downloading network tools", Style.RESET_ALL, sep='')
    
    data = list(await downloader.domains())

    print(Fore.RED, "Start writing domains", Style.RESET_ALL, sep='')
    async def write_blacklist(path, chunk_size=10000):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f'start writing domains to {path}')
        async with aiofiles.open(path, mode='w', encoding='utf-8') as f:
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i+chunk_size]
                await f.write('\n'.join(chunk) + '\n')
        logger.debug(f'finished writing domains to {path}')
    print(Fore.RED, "End writing domains", Style.RESET_ALL, sep='')
    
    async def write_bat_zp2():
        async with aiofiles.open('engine/zapret2/zapret2/zapret-winws/start.bat', mode='w') as f:
            await f.write(zp2_bat)
    
    await asyncio.gather(
        write_blacklist('engine/goodbyedpi/goodbyedpi/russia-blacklist.txt'),
        write_blacklist('engine/zapret2/zapret2/zapret-winws/list.txt'),
        write_bat_zp2()
    )
    
    print(Fore.GREEN, 'Finish', Style.RESET_ALL, sep='')
    return True