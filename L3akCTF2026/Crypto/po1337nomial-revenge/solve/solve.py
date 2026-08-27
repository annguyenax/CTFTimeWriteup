#!/usr/bin/env python3

import ssl
import socket
import re
from ast import literal_eval
from random import getrandbits, randbytes, randrange, setstate, shuffle
import sys

from randcrack import RandCrack


HOST = "po1337nomial-revenge.instances.ctf.l3ak.team"
PORT = 1337
n = 1337
x = 1337

sys.setrecursionlimit(n * n)


def recv_until(sock, marker: bytes) -> bytes:
    data = b""
    while marker not in data:
        chunk = sock.recv(65536)  # buffer lớn hơn
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data


def sendline(sock, data: bytes):
    sock.sendall(data + b"\n")


def main():
    print("[*] Đang kết nối...")
    context = ssl.create_default_context()
    raw_sock = socket.create_connection((HOST, PORT))
    sock = context.wrap_socket(raw_sock, server_hostname=HOST)

    # ========== 1. Lấy hệ số đã shuffle ==========
    recv_until(sock, b"> ")
    sendline(sock, b"1")

    # Nhận tất cả cho đến khi thấy prompt tiếp theo
    data = recv_until(sock, b"> ").decode()
    # Tìm dòng chứa list
    match = re.search(r"s:\s*(\[.*?\])", data, re.DOTALL)
    if not match:
        print("[-] Không tìm thấy list s")
        print(data[:500])
        sock.close()
        sys.exit(1)

    s = literal_eval(match.group(1))
    print(f"[+] Nhận được {len(s)} hệ số đã shuffle")

    # ========== 2. Evaluate ==========
    sendline(sock, b"2")
    recv_until(sock, b"x: ")
    sendline(sock, str(x).encode())

    data = recv_until(sock, b"> ").decode()
    match = re.search(r"y:\s*(\d+)", data)
    if not match:
        print("[-] Không tìm thấy y")
        print(data[:500])
        sock.close()
        sys.exit(1)

    y = int(match.group(1))
    print(f"[+] Nhận được y")

    # ========== Backtracking ==========
    def backtracking(i, v):
        if i == n:
            return v == 0
        r = v % x
        for c in list(m[r]):
            m[r].remove(c)
            a[i] = c
            if backtracking(i + 1, (v - c) // x):
                return True
            m[r].add(c)
        return False

    a = [1337] * n
    found = False

    print("[*] Đang backtracking (có thể mất 30-90 giây)...")
    for r in range(n):
        if r % 50 == 0:
            print(f"    Đang thử vị trí {r}/{n}...")

        si = s[r]
        s[r] = 1337

        m = {i: set() for i in range(x)}
        for b in s:
            m[b % x].add(b)

        if backtracking(0, y) and sorted(a) == sorted(s):
            s[r] = si
            found = True
            print(f"[+] Tìm thấy tại vị trí {r}")
            break

        s[r] = si

    if not found:
        print("[-] Không tìm được nghiệm. Hãy chạy lại.")
        sock.close()
        sys.exit(1)

    # Khôi phục hệ số gốc
    index = a.index(1337)
    missing = list(set(s) - (set(a) - {1337}))[0]
    a[index] = missing
    print(f"[+] Đã khôi phục hệ số gốc (vị trí bị thay: {index})")

    # ========== Crack MT19937 ==========
    print("[*] Đang crack random...")
    rc = RandCrack()
    for val in a[:624]:
        rc.submit(val)

    mt_state = [int("".join(map(str, rc.mt[i])), 2) for i in range(len(rc.mt))]
    setstate((3, (*mt_state, 0), None))

    # Kiểm tra
    assert all(a_i == getrandbits(32) for a_i in a[624:]), "Crack sai!"
    shuffled = a.copy()
    shuffle(shuffled)
    assert shuffled == s, "Shuffle không khớp!"
    assert index == randrange(0, n), "randrange không khớp!"
    print("[+] Crack random thành công!")

    # ========== 3. Lấy flag ==========
    sendline(sock, b"3")
    recv_until(sock, b"k: ")
    sendline(sock, randbytes(1337).hex().encode())

    data = recv_until(sock, b"\n").decode().strip()
    print(f"\n[+] FLAG: {data}")

    sock.close()


if __name__ == "__main__":
    main()