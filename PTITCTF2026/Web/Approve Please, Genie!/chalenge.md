# Approve Please, Genie!

500 pts — Web

A vocaloid song WITHOUT a depressing meaning behind it??? This is a very rare find

Status: **SOLVED** ✅

Flag: `PTITCTF{youtu.be/XKZIQlqVjjk?si=n3v3r_th0ught_css_c0uld_b_that_dang3r0us_ab8d8535d15b}`

Blind CSS exfiltration of the admin-visible hidden `#flag-holder` (CSP allows inline CSS).
The earlier failure was a dead/expired instance bot — on a fresh instance the technique worked,
leaking the flag one char per admin visit (resume across respawns). See `writeup/writeup.md`.
