#!/usr/bin/env python3
import subprocess
import re
import time
import urllib.request
import os

URL_FILE = "/Users/adamdimitrov/Development/budapest-adventures/data/active_tunnel_url.txt"

def run_tunnel():
    cmd = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=15", "-o", "ServerAliveCountMax=5", "-R", "80:127.0.0.1:3000", "nokey@localhost.run"]
    while True:
        print("[Tunnel] Starting SSH connection to localhost.run...")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        
        current_url = None
        for line in proc.stdout:
            print("[SSH]", line.strip())
            match = re.search(r'https://[a-zA-Z0-9.-]+\.lhr\.life', line)
            if match:
                current_url = match.group(0)
                print(f"[Tunnel] Detected active URL: {current_url}")
                os.makedirs(os.path.dirname(URL_FILE), exist_ok=True)
                with open(URL_FILE, 'w') as f:
                    f.write(current_url)
                break
                
        # Keepalive loop while process is running
        consecutive_errors = 0
        while proc.poll() is None:
            time.sleep(15)
            if current_url:
                try:
                    req = urllib.request.Request(f"{current_url}/", headers={'User-Agent': 'TunnelKeepAlive/1.0'})
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        if resp.status == 200:
                            print(f"[KeepAlive] Ping {current_url}/ OK")
                            consecutive_errors = 0
                except Exception as e:
                    consecutive_errors += 1
                    print(f"[KeepAlive] Ping error ({consecutive_errors}/3): {e}")
                    if consecutive_errors >= 3:
                        print("[Tunnel] 3 consecutive errors, restarting SSH connection...")
                        proc.kill()
                        break
                    
        print("[Tunnel] SSH process exited. Restarting in 3 seconds...")
        time.sleep(3)

if __name__ == '__main__':
    run_tunnel()
