# Evidence manifest — Warmy

| File | Purpose |
|---|---|
| local_run.txt | Local ret2win output (package flag.txt is fake for training) |
| checksec_notes.txt | Protections + key symbols |

Verification method:
1. Static: vuln uses gets into [rbp-0x40]; win() fopen/print flag.txt
2. Dynamic: payload A*0x48 + p64(win) → prints "The Flag: ..."