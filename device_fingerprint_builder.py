import platform
import uuid
import hashlib
import socket
import psutil
import time
from datetime import datetime

# Stylish ASCII Banner
BANNER = """
  ____          _          
 |  _ \ ___ ___| |__   ___ 
 | | | / __/ __| '_ \ / _ \\
 | |_| \__ \__ \ | | |  __/
 |____/|___/___/_| |_|____|
 
 Device Fingerprint Builder
 Coded by Pakistani Ethical Hacker Mr Sabaz Ali Khan
 Email: Sabazali236@gmail.com
"""

def get_system_info():
    """Collect system information for fingerprinting."""
    return {
        "os_name": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.architecture()[0],
        "machine": platform.machine(),
        "processor": platform.processor(),
        "node": platform.node(),
    }

def get_network_info():
    """Collect network-related information."""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])
        return {
            "hostname": hostname,
            "ip_address": ip_address,
            "mac_address": mac_address,
        }
    except Exception as e:
        return {"error": f"Network info error: {str(e)}"}

def get_hardware_info():
    """Collect hardware-related information."""
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return {
            "total_memory": f"{memory.total / (1024 ** 3):.2f} GB",
            "available_memory": f"{memory.available / (1024 ** 3):.2f} GB",
            "total_disk": f"{disk.total / (1024 ** 3):.2f} GB",
            "used_disk": f"{disk.used / (1024 ** 3):.2f} GB",
            "cpu_count": psutil.cpu_count(),
            "cpu_freq": f"{psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A'} MHz",
        }
    except Exception as e:
        return {"error": f"Hardware info error: {str(e)}"}

def get_timestamp():
    """Get current timestamp and timezone info."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "timezone": time.tzname[0],
    }

def generate_fingerprint():
    """Generate a unique device fingerprint by hashing collected attributes."""
    fingerprint_data = {
        **get_system_info(),
        **get_network_info(),
        **get_hardware_info(),
        **get_timestamp(),
    }
    
    # Convert dictionary to sorted string for consistent hashing
    fingerprint_string = ''.join(f"{k}:{v}" for k, v in sorted(fingerprint_data.items()))
    
    # Generate SHA-256 hash
    fingerprint_hash = hashlib.sha256(fingerprint_string.encode()).hexdigest()
    
    return {
        "fingerprint_data": fingerprint_data,
        "fingerprint_hash": fingerprint_hash,
    }

def main():
    """Main function to run the Device Fingerprint Builder."""
    print(BANNER)
    print("Generating Device Fingerprint...\n")
    
    result = generate_fingerprint()
    
    print("=== Device Fingerprint Details ===")
    for key, value in result["fingerprint_data"].items():
        if isinstance(value, dict):
            print(f"{key.replace('_', ' ').title()}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key.replace('_', ' ').title()}: {sub_value}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n=== Unique Fingerprint Hash ===")
    print(f"SHA-256 Hash: {result['fingerprint_hash']}")
    print("\nThank you for using Device Fingerprint Builder by Mr Sabaz Ali Khan!")

if __name__ == "__main__":
    main()