# Labyrinth Linguist evidence manifest

| File | Claim | Source | Repro |
|------|-------|--------|-------|
| `01_baseline.txt` | App up, default `Example text` | GET `/` | curl TARGET |
| `02_ssti_math.txt` | Velocity SSTI `#set($x=7*7)$x` → 49 | POST `text=` | curl |
| `03_rce_flag.txt` | `Runtime.exec('cat /flag.txt')` | POST Velocity chain | solve.py |
| `04_verify_replay.txt` | Same flag, independent run | solve.py | solve.py |

Flag verified: `HTB{f13ry_t3mpl4t35_fr0m_th3_d3pth5!!_a3ce0020cb78a323c28c8b6d8769d3ed}`
