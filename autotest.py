from pathlib import Path
import subprocess
import psutil
import telemetry
import asyncio
import time

p = Path(__file__).parent
engine = Path(p / "engine")
gb = Path(engine / "goodbyedpi" / "goodbyedpi")
zp = Path(engine / "zapret" / "zapret")
zp2 = Path(engine / "zapret2" / "zapret2")


class test():
    def __init__(self, gb_path, zp_path, zp2_path, zapret_alt: int, zp2_params: str):
        self.gb_file = Path(gb_path / "1_russia_blacklist.cmd")
        self.zp_file = Path(zp_path / f"general (ALT{zapret_alt}).bat")
        self.zp2_file = Path(zp2_path / "")
        self.zp2_settings = zp2_params
    
    def kill(process_name: str): # for end
        for proc in psutil.process_iter():
            if proc.name() == process_name:
                proc.kill()
    
    
    def goodbyedpi(self): # start goodbyedpi
        gb_data = subprocess.run([f"'{self.gb_file}'"])
        

    def zapret(self): # start zapret
        zp_data = subprocess.run([f"'{self.zp_file}'"])
    
    def zapre2(self): # eto pizdec
        pass
    
    def warp(self):
        warp_data = subprocess.run(['warp-cli', 'connect'])
        time.sleep(5)
        country_data = asyncio.run(telemetry.run())['geo_full']['country']['names']['en']
        print(country_data)
    

s = test(gb, zp, zp2, 3, "None")
s.goodbyedpi()
s.warp()