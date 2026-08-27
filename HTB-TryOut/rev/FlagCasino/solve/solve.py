#!/usr/bin/env python3
# FlagCasino (HTB TryOut, rev) -- solver
#
# Binary logic (objdump of `casino`, ELF x86-64, symbols present):
#   main:
#     for i in 0 .. 0x1c (29 iterations):          ; 29-char flag
#         printf("> ")                              ; 0x20f9
#         scanf("%c", &c)                           ; format "%c" at 0x20fc
#         if (scanf != 1) exit(-1)
#         srand(c)                                  ; seed = bet char
#         if (rand() != check[i]) {                 ; check[] = 29 DWORDs @ VA 0x4080
#             puts("[ * INCORRECT * ]");
#             puts("[ *** ACTIVATING SECURITY SYSTEM - PLEASE VACATE *** ]");
#             exit(-2);
#         }
#         puts("[ * CORRECT *]");
#     puts("[ ** HOUSE BALANCE $0 - PLEASE COME BACK LATER ** ]");
#
# => flag = the 29 chars c_i such that glibc srand(c_i); rand() == check[i].
# We match against the ground-truth glibc rand table (evidence/rand_table.txt)
# generated on real glibc with `srand(s); rand()` for s in 0..255.

import os

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence")

# --- load expected rand() values (from .data @ VA 0x4080) ---
with open(os.path.join(EV, "check_array.txt")) as f:
    check = [int(tok, 16) for line in f if not line.strip().startswith("#")
             for tok in line.split()]
assert len(check) == 29, len(check)

# --- load glibc ground-truth table: seed -> first rand() ---
rand_of = {}
with open(os.path.join(EV, "rand_table.txt")) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        s, v = line.split()
        rand_of[int(s)] = int(v)

# --- solve: invert the table for printable chars ---
seed_of = {}
for s, v in rand_of.items():
    seed_of.setdefault(v, []).append(s)

flag = []
for i, want in enumerate(check):
    cands = [s for s in seed_of.get(want, []) if 0x20 <= s <= 0x7E]
    if not cands:
        raise SystemExit(f"position {i}: value {want:#x} has no printable seed")
    # expect exactly one printable candidate per position
    flag.append(cands[0])
    if len(cands) > 1:
        print(f"note: position {i} has {len(cands)} candidates {cands}")

flag_str = "".join(chr(c) for c in flag)
print("recovered char codes:", [hex(c) for c in flag])
print("flag candidate      :", flag_str)

# --- independent replay verification ---
ok = all(rand_of[ord(ch)] == want for ch, want in zip(flag_str, check))
print("deterministic replay (srand(char); rand() == check[i]):",
      "PASS" if ok else "FAIL")
assert ok
assert flag_str.startswith("HTB{") and flag_str.endswith("}"), flag_str
print("FINAL FLAG:", flag_str)
