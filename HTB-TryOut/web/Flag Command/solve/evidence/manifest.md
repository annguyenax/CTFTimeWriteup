# Flag Command evidence manifest

| File | Claim | Source | Repro |
|------|-------|--------|-------|
| `01_baseline.txt` | Flask app, JS assets | GET `/` | curl TARGET |
| `js_commands.js.txt` | UI commands only; no flag | GET `/static/terminal/js/commands.js` | curl |
| `js_main.js.txt` | `/api/options` + `/api/monitor`; checks `secret` + `HTB{` | GET `.../main.js` | curl |
| `02_api_options.txt` | Secret command list | GET `/api/options` | curl |
| `03_api_monitor_secret.txt` | Flag in JSON message | POST `/api/monitor` | solve.py |
| `04_verify_replay.txt` | Same flag on replay | POST `/api/monitor` | curl |

Flag verified: `HTB{D3v3l0p3r_t00l5_4r3_b35t_wh4t_y0u_Th1nk??!_849b56a26793e9181ffd1cc6ebe163f3}`
