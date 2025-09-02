import platform
import os
import psutil
import socket
import requests


def get_system_info():
    info = {}

    # System / OS
    info["system"] = platform.system()
    info["node_name"] = platform.node()
    info["release"] = platform.release()
    info["version"] = platform.version()
    info["machine"] = platform.machine()
    info["processor"] = platform.processor()
    info["cpu_count"] = os.cpu_count()

    # Hardware usage
    info["cpu_usage_percent"] = psutil.cpu_percent(interval=1)
    info["memory"] = dict(psutil.virtual_memory()._asdict())
    info["disk"] = dict(psutil.disk_usage('/')._asdict())
    info["boot_time"] = psutil.boot_time()

    # Network - local IP
    hostname = socket.gethostname()
    info["hostname"] = hostname
    try:
        info["local_ip"] = socket.gethostbyname(hostname)
    except Exception:
        info["local_ip"] = None

    # Network - public IP
    try:
        info["public_ip"] = requests.get("https://api4.ipify.org?format=json", timeout=5).json()["ip"]
    except Exception:
        info["public_ip"] = None

    return info


# Example usage
if __name__ == "__main__":
    system_info = get_system_info()
    for k, v in system_info.items():
        print(f"{k}: {v}")
