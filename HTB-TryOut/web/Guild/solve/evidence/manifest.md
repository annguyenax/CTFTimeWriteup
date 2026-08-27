# Guild evidence manifest

| File | Claim | Source | Repro |
|------|-------|--------|-------|
| `01_login.txt` | Account + session | POST `/signup` `/login` | solve.py |
| `02_upload.txt` | JPEG + EXIF Artist payload stored | POST `/verification` | solve.py |
| `03_ssti_math.txt` | Jinja2 SSTI via bio `%s` | GET `/user/<name>` | solve.py |
| `04_ssti_email.txt` | Admin email leaked (`User.query.get(1)`) | GET `/user/<name>` | solve.py |
| `05_reset.txt` | Reset token = SHA256(email) | POST `/forgetpassword` `/changepasswd/<h>` | solve.py |
| `06_admin_login.txt` | Admin session | POST `/login` | solve.py |
| `07_admin_page.txt` | verification_id=1 user_id=2 | GET `/admin` | solve.py |
| `08_verify.txt` | Unfiltered SSTI on EXIF Artist | POST `/verify` | solve.py |
| `09_verify_replay.txt` | Same flag, independent session | POST `/verify` | curl/pwsh |

Flag verified: `HTB{mult1pl3_lo0p5_mult1pl3_h0les_c7d6e9e6f977892138674af6b827a0ad}`
