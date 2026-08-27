# Evidence manifest — carnival_game

| File | Claim supported | Source/Tool | Reproduction | Why kept |
|------|-----------------|-------------|--------------|----------|
| ../solve.py | Network solver: recover time-seed from commitment, predict rolls | hand-written | `python solve.py <host> <port>` (live) | Real exploit |
| ../local_test.py | End-to-end proof against the exact server code offline | subprocess harness | copy files/carnival-game.py -> server.py, add flag.txt, `python local_test.py` | Verifies technique |
| local_run.txt | Captured winning run printing the (dummy) flag | local_test.py | as above | Evidence of win |

## Result
- Vulnerability: `seed = random.Random(int(time.time())).randbytes(16).hex()` — the
  seed depends only on the connection time in whole seconds. `commitment=sha256(seed)`
  is published, which lets us confirm the recovered seed.
- Exploit: brute int(time.time()) in a small window, recompute the seed, match the
  commitment, then compute `roll(seed, round)=int(sha256(f"{seed}-{round}"),16)%100`
  and guess 5 in a row.

## Verification
`local_test.py` runs the exact server code and wins 5/5, printing the flag:
`Congratulations! Here's your flag b'LITCTF{fake_flag_for_local_test}'` (dummy).

## Note on the real flag
This is a remote-only challenge; the real flag lives in the server's flag.txt.
Offline (no connection / no submission) the real flag was NOT captured and is NOT
fabricated. Running solve.py against the live service would print it.
