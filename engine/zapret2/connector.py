import subprocess
from pathlib import Path
from elevate import elevate
import asyncio
import aiofiles

elevate()

bat_text = r"""@echo off
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


dir_now = Path(__file__).parent
bat_file = Path(dir_now / 'zapret2' / 'zapret-winws' / 'start.bat')


async def ensure_bat_exists():
    if not bat_file.is_file():
        bat_file.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(bat_file, mode='w', encoding='utf-8') as f:
            await f.write(bat_text)
    return bat_file.is_file()



async def connect():
    if await ensure_bat_exists():
        subprocess.run([str(bat_file)], shell=True)
    else:
        pass

async def run():
  await ensure_bat_exists()
  await connect()