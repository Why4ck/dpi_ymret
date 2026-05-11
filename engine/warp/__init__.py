import subprocess
import sys
import os

# from import logger
current_dir = os.path.dirname(os.path.abspath(__file__)) # dirs
parent_dir = os.path.dirname(current_dir) # engine dir
root_dir = os.path.dirname(parent_dir) # project dir

sys.path.append(root_dir)

from logger import setup_logger

logger = setup_logger()

def is_warp_installed() -> bool:
    """Проверка наличия warp-cli"""
    try:
        output = subprocess.check_output(
            ["warp-cli", "-V"],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5
        )
        if "warp-cli" in output.lower():
            logger.info("Successfully | Warp found")
            return True
        return False
    except FileNotFoundError:
        logger.error("ERROR: Cloudflare WARP not found")
        logger.info("Download warp here -> https://1.1.1.1")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unknown error while checking Warp: {e}")
        sys.exit(1)


def main():
    is_warp_installed()

    # check register
    try:
        show = subprocess.check_output(
            ['warp-cli', 'registration', 'show'],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10
        )
    except subprocess.CalledProcessError as e:
        show = e.output if isinstance(e.output, str) else e.output.decode('utf-8', errors='ignore')
    except Exception as e:
        logger.error(f"Failed to check registration: {e}")
        show = ""

    if "Error" in show or "not registered" in show.lower():
        logger.info("Warp account creating...")

        for attempt in range(2):  # 2 try
            result = subprocess.run(
                ['warp-cli', 'registration', 'new'],
                capture_output=True,
                text=True,
                timeout=15
            )

            output = (result.stdout + result.stderr).lower()

            if "success" in output:
                logger.info("Warp account created successfully")
                return
            elif "timeout" in output or "ipc call hit a timeout" in output:
                logger.warning(f"Timeout on attempt {attempt + 1}. Restarting WARP...")

                # kill process
                subprocess.run(['taskkill', '/f', '/im', 'Cloudflare WARP.exe'],
                             capture_output=True, shell=True)

                # delete old account
                subprocess.run(['warp-cli', 'registration', 'delete'],
                             capture_output=True, text=True)

                continue  # again
            else:
                logger.error(f"Failed to create account. Output: {result.stdout + result.stderr}")
                break

        logger.error("Failed to create Warp account after retries")
        sys.exit(1)
    else:
        logger.info("Warp account was created earlier")


main()