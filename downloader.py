import asyncio
import aiofiles
import aiohttp
from links import * # <- here all base links for work
import shutil
import os
from pathlib import Path
import subprocess
import psutil
import requests

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

# Global request settings
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}
TIMEOUT = aiohttp.ClientTimeout(total=10)
from logger import setup_logger


logger = setup_logger()

dir_now = Path(__file__).parent # dir

async def fetch_data(url: str, name: str) -> str:
    logger.info(f'start downloading {name}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                response.raise_for_status()
            except:
                response.raise_for_status()
            
            
            content = await response.text()
            logger.debug(f'end download {name}')
            return content


async def domains():
      """
      The domains function loads all domains from:
      goodbyedpi, zapret, zapret_info
      This function is async, and its subfunctions are also async
      """

      # goodbyedpi domains
      goodbyedpi_txt = await fetch_data(gb_txt, 'goodbyedpi domains')

      # zapret-info domains
      zp_i_txt = await fetch_data(zi_txt, 'zapret-info domains')

      # zapret domains (all 3 requests)
      zapret_1_txt = await fetch_data(zp_txt_1, 'zapret 1')
      zapret_2_txt = await fetch_data(zp_txt_2, 'zapret 2')
      zapret_3_txt = await fetch_data(zp_txt_3, 'zapret 3')
      all = zapret_1_txt + '\n' + zapret_2_txt + '\n' + zapret_3_txt

      # Combine all domains
      data = goodbyedpi_txt + '\n' + zp_i_txt + '\n' + all
      return set(data.splitlines())  # return domains



async def get_dir(response_stream, zip_name, extract_dir):
    logger.debug('start getting normalized dir')
    if os.path.exists(extract_dir):
        logger.debug(f'remove tree of {extract_dir}')
        shutil.rmtree(extract_dir)
    
    
    temp_dir = Path(dir_now / "temp_unpack")
    logger.debug('create temp dir for extract zip')
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(extract_dir, exist_ok=True)

    logger.debug('open zip for extract')
    async with aiofiles.open(zip_name, mode='wb') as f:
        async for chunk in response_stream.iter_chunked(65536):
            await f.write(chunk)

    await asyncio.to_thread(shutil.unpack_archive, zip_name, temp_dir)
    logger.debug('extract zip')
    items = os.listdir(temp_dir)
    
    if items:
        logger.debug('get dir normalized')
        nested_folder = os.path.join(temp_dir, items[0])
        
        for item in os.listdir(nested_folder): # normalizing dir
            s = os.path.join(nested_folder, item)
            d = os.path.join(extract_dir, item)
            shutil.move(s, d)

    shutil.rmtree(temp_dir)
    logger.debug('delete temp dir')
    os.remove(zip_name)
    logger.debug('remove zip')

async def obfs():
    """
The obfs func loads all obfs tools:
goodbyedpi, zapret, zapret2

This function is async, and its subfunctions are also async

Dont use one session because github block multy download
    """
    
    async def goodbyedpi():
        logger.debug('start download goodbyedpi')
        async with aiohttp.ClientSession() as session:
            logger.info('open aiohttp session')
            async with session.get(gb_link) as response:
                await get_dir(response.content, Path(dir_now / 'goodbyedpi.zip'), Path(dir_now / 'engine/goodbyedpi/goodbyedpi'))
            
    async def zapret():
        logger.debug('start download zapret')
        async with aiohttp.ClientSession() as session:
            logger.info('open aiohttp session')
            async with session.get(zapret_link) as response:
                logger.debug('download and normalizing zapret')
                await get_dir(response.content, Path(dir_now / 'zapret.zip'), Path(dir_now / 'engine/zapret/zapret'))
        logger.debug('successfully zapret download and normalizing')
        
    async def zapret2():
        logger.debug('start download zapret2')
        async with aiohttp.ClientSession() as session:
            logger.info('open aiohttp session')
            async with session.get(zapret2_link) as response:
                logger.debug('download and normalizing zapret2')
                await get_dir(response.content, Path(dir_now / 'zapret2.zip'), Path(dir_now / 'engine/zapret2/zapret2'))
        logger.debug('successfully zapret2 download and normalizing')
                    
    logger.debug('start downloading utils')
    try:
        await goodbyedpi()
    except:
        await goodbyedpi()
    
    try:
        await zapret()
    except:
        await zapret()
        
    try:
        await zapret2()
    except:
        await zapret2()
        

    logger.debug('end downloading utils')

async def warp():
    async def check():
        logger.info('start check warp')
        result = subprocess.run(['warp-cli', '-V'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode
    
    def download():
        if system == 'Windows':
            logger.debug('start download warp.msi installer')
            data = requests.get(warp_download_win).content # download warp
            logger.debug('end download warp.msi installer')
            with open('warp.msi', mode='wb') as f:
                logger.debug('start write byte code to .msi file')
                f.write(data) # get .msi file
                logger.debug('end write byte code to .msi file')
            
            logger.debug('start warp.msi')
            subprocess.run(['msiexec', '/i', f'{dir_now}/warp.msi'], shell=True) # start .msi file
            logger.debug('end warp.msi')
            
        
        elif system == 'Linux':
            logger.debug('run sudo apt-get update')
            subprocess.run(['sudo', 'apt-get', 'update'], check=True) # update
            logger.debug('run sudo apt-get install -y cloudflare-warp')
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'cloudflare-warp'], check=True) # download warp
            
        return True
    
    warp_is_installed = await check()

    # 0 - Success, not 0 (1 OR 127) - error
    if warp_is_installed != 0:
        for i in range(3):
            res = download()
            if res == True:
                break
    
    
    # kill warp process
    subprocess.run(['msiexec', '/i', 'warp.msi'], check=True)


    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == "Cloudflare WARP.exe":
                proc.terminate()
                proc.wait(timeout=3)
                logger.debug('kill warp app process')
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.critical(f'CRITICAL ERROR: {e}')

    # delete file
    if system == 'Windows':
        try:
            os.remove('warp.msi')
            logger.debug('deleted warp.msi')
        except OSError as e:
            logger.critical(f'CRITICAL ERROR: {e}')

async def wiresock():
    # Start zapret2
    async def start():
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
        
        await connect()
    
    await start()
    
    
    logger.debug('Start download WireSock')
    async with aiohttp.ClientSession() as session:
        logger.info('open aiohttp session')
        async with session.get(wiresock_link) as response:
            logger.debug('Download and write WireSock')
            async with aiofiles.open('wiresock_installer.exe', mode='wb') as f: # async with Triad
                await f.write(await response.read())
            logger.debug('Start write WireSock')
    logger.debug('End download WireSock')
    
    subprocess.run(['WireSockConnect.exe'], shell=True)

    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == "WireSockConnect.exe":
                proc.terminate()
                proc.wait(timeout=3)
                logger.debug('kill warp app process')
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.critical(f'CRITICAL ERROR: {e}')

    # delete file
    if system == 'Windows':
        try:
            os.remove('WireSockConnect.exe')
            logger.debug('deleted WireSockConnect.exe')
        except OSError as e:
            logger.critical(f'CRITICAL ERROR: {e}')






# async def get_mmdb(response, path):
#     async with aiofiles.open(path, mode='wb') as f:
#         async for chunk in response.content.iter_chunked(65536):
#             await f.write(chunk)

# async def mmdb_downloader(url, name):
#     logger.debug(f'start downloadding {url}')
#     async with aiohttp.ClientSession() as session:
#         logger.info('open aiohttp session')
#         async with session.get(url) as response:
#             if response.status == 200:
#                 await get_mmdb(response, f'telemetry/{name}.mmdb')
#                 logger.debug(f'successfully download mmbd from {url}')
#             else:
#                 logger.critical(f'error connect to {url}')

# async def telemetry():
#     Path("telemetry/").mkdir(parents=True, exist_ok=True)
#     await asyncio.gather(mmdb_downloader(asn, 'asn'), mmdb_downloader(city, 'city'))


