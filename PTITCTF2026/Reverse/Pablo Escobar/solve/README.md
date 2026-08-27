# Pablo Escobar — solvers

**Status:** reverse + inbox dump work. Flag not recovered. Resume from `..\notes\SESSION.md`.

## Decrypt config.enc

Needs Python `cryptography`.

From extracted scratch:

```powershell
python decrypt_config.py --exe D:\download\ctf-scratch\ptitctf2026_pablo_escobar\Tool.exe --enc D:\download\ctf-scratch\ptitctf2026_pablo_escobar\config.enc
```

From `dist.zip` after extract:

```powershell
python decrypt_config.py --exe Tool.exe --enc config.enc
```

Expected URL: `http://144.79.188.36:6500/`

## Dump inbox as luongvd

```powershell
python fetch_inbox.py --out D:\download\ctf-scratch\ptitctf2026_pablo_escobar\inbox
```

Cached copies (no live server needed to review): `..\notes\inbox\1.jpg` `2.jpg` `4.jpg` and `..\notes\evidence\inbox.json`.

Id 3 stays 403 for this user.
