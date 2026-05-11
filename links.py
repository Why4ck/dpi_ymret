import platform

# raw zapret2 links
zapret2_win = "https://github.com/bol-van/zapret-win-bundle/archive/refs/heads/master.zip"
zapret2_linux = "http://github.com/bol-van/zapret2/archive/refs/heads/main.zip"

system = platform.system() # get sys

# sorted by system zapret2 links
if system == 'Windows':
    zapret2_link = zapret2_win
elif system == 'Linux':
    zapret2_link = zapret2_linux
else:
    raise NotImplementedError(f"Unsupported operating system: {system}. Only Windows and Linux are supported.")

# universal links
zapret_link = "https://github.com/flowseal/zapret-discord-youtube/archive/refs/heads/main.zip"
gb_link = "https://github.com/ValdikSS/GoodbyeDPI/releases/download/0.2.3rc3/goodbyedpi-0.2.3rc3-2.zip"

wiresock_link = 'https://wiresock.net/_api/download-release.php?product=wiresock-secure-connect&platform=windows_x64&version=3.4.6.1'

# warp
warp_link = "https://one.one.one.one/"
warp_linux = "https://pkg.cloudflareclient.com/"
warp_win = "https://1111-releases.cloudflareclient.com/win/latest"

warp_download_win = "https://downloads.cloudflareclient.com/v1/download/windows/ga"
warp_download_linux_command = "sudo apt-get update && sudo apt-get install cloudflare-warp"

# TXTs
gb_txt = "https://raw.githubusercontent.com/rdavydov/goodbyedpi-win/refs/heads/main/russia-blacklist.txt"
zi_txt = "https://raw.githubusercontent.com/zapret-info/z-i/refs/heads/master/nxdomain.txt"
zp_txt_1 = "https://raw.githubusercontent.com/Flowseal/zapret-discord-youtube/main/lists/list-general.txt"
zp_txt_2 = "https://raw.githubusercontent.com/Flowseal/zapret-discord-youtube/refs/heads/main/lists/list-exclude.txt"
zp_txt_3 = "https://raw.githubusercontent.com/Flowseal/zapret-discord-youtube/refs/heads/main/lists/list-google.txt"

# telemetry
asn = 'https://git.io/GeoLite2-ASN.mmdb'
city = 'https://git.io/GeoLite2-City.mmdb'