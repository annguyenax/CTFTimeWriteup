#!/usr/bin/env python3
"""
LIT2026 / crypto / carnival_game

Server logic (carnival-game.py):
    seed = random.Random(int(time.time())).randbytes(16).hex()
    print("commitment:" + sha256(seed))
    roll(seed, round) = int(sha256(f"{seed}-{round}"),16) % 100
    # win by guessing 5 rolls in a row -> prints flag

Vulnerability: the seed is fully determined by int(time.time()) (Mersenne Twister
seeded with the current time in SECONDS). The published commitment sha256(seed)
lets us CONFIRM a guess. So when we connect we know the approximate time; we brute
a small window of integer seconds, recompute random.Random(t).randbytes(16).hex(),
hash it, and match the commitment. That recovers the exact seed, after which every
roll is predictable and we win 5/5.

Usage (live):  python solve.py 136.115.87.65 31783
This is the network solver; it was verified end-to-end against a local copy of the
exact server code (see solve/evidence/).
"""
import socket, hashlib, random, time, sys


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def roll(seed, rnd):
    return int(sha(f"{seed}-{rnd}"), 16) % 100


def recover_seed(commitment, approx_now, window=3 * 24 * 3600):
    # Brute a WIDE window of integer seconds around our clock. The server's clock
    # may differ from ours by minutes/hours, so a tight window can miss it; a few
    # days each way is still only ~500k cheap hashes.
    for delta in range(0, window):
        for t in (approx_now + delta, approx_now - delta):
            if sha(random.Random(t).randbytes(16).hex()) == commitment:
                return random.Random(t).randbytes(16).hex(), t
    return None, None


def main(host, port):
    s = socket.create_connection((host, port))
    f = s.makefile('rw', buffering=1)
    approx_now = int(time.time())

    commit_line = f.readline().strip()               # "commitment:<hex>"
    commitment = commit_line.split("commitment:")[1]
    f.readline()                                      # banner line

    seed, t = recover_seed(commitment, approx_now)
    if seed is None:
        print("[-] failed to recover seed; widen window"); return
    print(f"[+] recovered seed (t={t}): {seed}")

    for rnd in range(5):
        f.readline()                                  # "round N, streak .../5, ..."
        g = roll(seed, rnd)
        f.write(f"{g}\n"); f.flush()
        print(f"[>] round {rnd}: guessed {g} -> {f.readline().strip()}")
    # remaining output contains the flag
    print(s.recv(4096).decode(errors='replace'))


if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else '136.115.87.65'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 31783
    main(host, port)
