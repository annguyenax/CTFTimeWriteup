# Blueprint Heist evidence manifest

| File | Claim | Source | Repro |
|------|-------|--------|-------|
| `01_env.txt` | Live `.env` (secret ≠ zip) | wkhtmltopdf `data:` + XHR `file:///app/.env` | solve.py |
| `02_sqli.txt` | GraphQL SQLi OUTFILE (no iterable = write ran) | GET `/graphql` via PDF SSRF | solve.py |
| `03_ssti.txt` | 404.ejs SSTI ran `/readflag` | GET unknown path | solve.py |
| `04_verify_replay.txt` | Same flag, independent 404 | GET `/verify-flag-replay-404` | curl |

Flag verified: `HTB{ch41ning_m4st3rs_b4y0nd_1m4g1nary_3dfb9cf1df1e4de4cddde2d22493e0fd}`
