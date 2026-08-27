# HTB Proxy evidence manifest

| File | Claim | Source | Repro |
|------|-------|--------|-------|
| `01_baseline.txt` | Proxy up, `Server: HTB proxy` | GET `/` | curl |
| `02_server_status.txt` | Container IP `10.244.40.122` | GET `/server-status` | curl |
| `03_ssrf_10-244-40-122.sslip.io.txt` | Host dash-IP.sslip.io:5000 reaches Express | POST `/getAddresses` | solve.py |
| `04_smuggle.txt` | CL-split smuggle hits `/flushInterface` | pipelined POST | solve.py |
| `05_index_after.txt` | `/flag*` copied over index.html | GET `/` | solve.py |
| `06_verify_replay.txt` | Same flag, independent GET `/` | GET `/` | curl |

Flag verified: `HTB{r3inv3nting_th3_wh331_c4n_cr34t3_h34dach35_edcec11fd46a9fe5e9820f74ebb11c6a}`
