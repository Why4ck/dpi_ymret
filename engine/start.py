from goodbyedpi import connecter as g
from zapret import connecter as z
from warp import connecter as w
import asyncio
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import psutil

process_names = [
    'v2rayN.exe', 'v2ray.exe',
    'xray.exe',
    'happ.exe', 'happd.exe',
    'v2raytun.exe',
    'nekoray.exe',
    'Matsuri.exe', 'SagerNet.exe',
    'clash-win64.exe', 'clash-windows-amd64.exe',
    'clash-verge.exe', 'clash-verge-service.exe',
    'FlClash.exe',
    'koala-clash.exe',
    'Hiddify.exe', 'HiddifyApp.exe',
    'nekobox.exe',
    'wireguard.exe', 'wg.exe',
    'openvpn.exe', 'openvpnserv.exe', 'openvpn-gui.exe',
    'Shadowsocks.exe',
    'amneziavpn.exe', 'vplanc.exe',
    'Outline.exe', 'Outline Manager.exe',
    'ProtonVPN.exe', 'Surfshark.exe', 'NordVPN.exe', 'ExpressVPN.exe',
    'warp-svc.exe', 'Cloudflare WARP.exe',
    'zapret.exe', 'zapretKVN.exe',
    'goodbyedpi.exe',
    'byedpi-service',
    'UltraSurf.exe',
    'winws.exe', 'winwsw2.exe', 'zapret.exe', 'zapret2.exe',
]

for proc in psutil.process_iter(['name']):
    try:
        if proc.info['name'] in process_names:
            proc.kill()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass


async def start():
    global country
    await g.run()
    data = await w.main()
    
    if data:
        return True
    else:
        await g.kill()
        await w.disconnect()
        return False
    
asyncio.run(start())