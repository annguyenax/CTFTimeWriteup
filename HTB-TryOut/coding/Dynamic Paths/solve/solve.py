#!/usr/bin/env python3
"""
Dynamic Paths (HTB Try Out, easy coding) — solver.

Given t=100 grids (i x j, 2 <= i,j <= 100, values 1..50), start top-left,
move only down/right, minimize sum of visited cells. Classic grid DP:
dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1]).
"""

import re
import socket

HOST = "154.57.164.78"
PORT = 30321


def min_path_sum(grid, i, j):
    dp = [0] * j
    for r in range(i):
        for c in range(j):
            if r == 0 and c == 0:
                dp[c] = grid[r][c]
            elif r == 0:
                dp[c] = dp[c - 1] + grid[r][c]
            elif c == 0:
                dp[c] = dp[c] + grid[r][c]
            else:
                dp[c] = grid[r][c] + min(dp[c], dp[c - 1])
    return dp[j - 1]


def main():
    s = socket.socket()
    s.settimeout(20)
    s.connect((HOST, PORT))
    buf = b""

    def recv_until(marker=b"> ", timeout=20):
        nonlocal buf
        s.settimeout(timeout)
        while marker not in buf:
            try:
                d = s.recv(8192)
            except socket.timeout:
                break
            if not d:
                break
            buf += d
        return buf

    banner = recv_until()
    print(banner.decode("latin1", "replace")[-300:])

    for test in range(1, 101):
        # read until a fresh prompt or enough data for this test
        data = recv_until(b"> ")
        txt = data.decode("latin1", "replace")
        # isolate the current test block: after the last "Test X/100"
        blocks = re.findall(r"Test \d+/100\s*\n(.*?)>", txt, re.S)
        if not blocks:
            # fallback: parse from the last dims line
            nums = list(map(int, re.findall(r"\d+", txt)))
            # need at least dims + grid; take last i*j+2 numbers
            if len(nums) >= 4:
                i, j = nums[-2 - nums[-1] * nums[-2] :][:2] if False else (nums[-2 - (nums[-1] if False else 0) * 0], 0)
            raise RuntimeError(f"cannot parse block on test {test}: {txt[-400:]}")
        block = blocks[-1].strip()
        allnums = list(map(int, re.findall(r"\d+", block)))
        i, j = allnums[0], allnums[1]
        vals = allnums[2 : 2 + i * j]
        if len(vals) < i * j:
            raise RuntimeError(f"not enough grid values on test {test}: got {len(vals)}, need {i*j}")
        grid = [vals[r * j : (r + 1) * j] for r in range(i)]
        ans = min_path_sum(grid, i, j)
        s.sendall(f"{ans}\n".encode())
        buf = b""  # reset buffer each round (answers interleave with prompts)
        if test % 20 == 0:
            print(f"[*] test {test}/100 done (ans={ans})")

    # read the remaining output (flag)
    s.settimeout(20)
    out = b""
    try:
        while True:
            d = s.recv(8192)
            if not d:
                break
            out += d
    except socket.timeout:
        pass
    s.close()
    print("=== FINAL OUTPUT ===")
    print(out.decode("latin1", "replace"))
    flag = re.search(r"HTB\{[^}]+\}", out.decode("latin1", "replace"))
    if flag:
        print("FLAG:", flag.group(0))
        with open("final_flag.txt", "w") as f:
            f.write(flag.group(0) + "\n")


if __name__ == "__main__":
    main()
