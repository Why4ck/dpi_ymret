import subprocess
import os
import glob
import time
import re
from elevate import elevate

elevate()

def find_conf():
    root = os.path.dirname(os.path.abspath(__file__))
    files = glob.glob(os.path.join(root, '*.conf'))
    if files:
        return files[0]
    return None

def clean_conf(path):
    """
    Очищает AmneziaWG-поля, оставляя чистый WireGuard формат.
    """
    with open(path, 'r') as f:
        lines = f.readlines()
    
    # Поля, которые WireGuard НЕ понимает
    amnezia_fields = ['S1', 'S2', 'S3', 'S4', 'Jc', 'Jmin', 'Jmax', 
                      'H1', 'H2', 'H3', 'H4', 'I1', 'I2']
    
    cleaned = []
    for line in lines:
        # Пропускаем строки с Amnezia-полями
        if any(line.strip().startswith(f"{field} =") for field in amnezia_fields):
            continue
        cleaned.append(line)
    
    # Сохраняем очищенный конфиг с суффиксом _clean
    clean_path = path.replace('.conf', '_clean.conf')
    with open(clean_path, 'w') as f:
        f.writelines(cleaned)
    
    return clean_path

def connect():
    conf = find_conf()
    if not conf:
        raise FileNotFoundError('.conf not found')
    
    # Очищаем от Amnezia-полей
    clean_path = clean_conf(conf)
    
    wg = r'C:\Program Files\WireGuard\wireguard.exe'
    name = os.path.splitext(os.path.basename(clean_path))[0]
    
    # Убиваем старую службу
    subprocess.run([wg, '/uninstalltunnelservice', name], capture_output=True)
    time.sleep(1)
    
    # Устанавливаем новую
    result = subprocess.run(
        [wg, '/installtunnelservice', clean_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"WireGuard error: {result.stderr}")
    
    time.sleep(2)
    subprocess.run(['sc', 'start', name], check=True)

def disconnect():
    wg = r'C:\Program Files\WireGuard\wireguard.exe'
    root = os.path.dirname(os.path.abspath(__file__))
    
    for conf in glob.glob(os.path.join(root, '*_clean.conf')):
        name = os.path.splitext(os.path.basename(conf))[0]
        subprocess.run(['sc', 'stop', name], capture_output=True)
        subprocess.run([wg, '/uninstalltunnelservice', name], capture_output=True)

if __name__ == '__main__':
    connect()