#!/usr/bin/env python3
"""
Offline end-to-end verification of the carnival_game exploit.

Runs the EXACT server code (files/carnival-game.py) as a subprocess with a dummy
flag.txt, then drives it with the seed-recovery attack and confirms it wins and
receives the (dummy) flag. This proves the technique without touching the remote.

Run from this directory with a copy of the server as ./server.py and a ./flag.txt,
or adapt paths. See evidence/manifest.md for the captured run.
"""
import subprocess, hashlib, random, time

def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def roll(seed, r): return int(sha(f"{seed}-{r}"), 16) % 100

def main():
    t0 = int(time.time())
    p = subprocess.Popen(['python3', 'server.py'], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, bufsize=1, text=True)
    commit = p.stdout.readline().strip().split('commitment:')[1]
    p.stdout.readline()  # banner
    seed = None
    for t in range(t0 + 2, t0 - 60, -1):
        c = random.Random(t).randbytes(16).hex()
        if sha(c) == commit:
            seed = c; break
    assert seed, "seed not recovered"
    for r in range(5):
        p.stdin.write(f"{roll(seed, r)}\n"); p.stdin.flush()
        p.stdout.readline()                 # "round r ...: roll was X, streak = r+1"
    out, _ = p.communicate(input="q\n", timeout=10)  # flush remaining incl. flag line
    won = 'Congratulations' in out
    for line in out.splitlines():
        if 'Congratulations' in line:
            print(line.strip())
    print("WIN:", won)

if __name__ == '__main__':
    main()
