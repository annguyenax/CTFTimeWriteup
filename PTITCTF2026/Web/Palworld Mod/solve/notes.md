# Palworld Mod — evidence notes

Instances seen: `144.79.188.39:35964`, `:36310`, `:36534`.

## Stack
- Backend: Django 4.2.11 + DRF 3.15.1 + djangorestframework-simplejwt 5.3.1 + daphne (ASGI) + drf-spectacular.
- Frontend: Angular SPA served by nginx; nginx proxies `/api/` and `/media/` to daphne on `127.0.0.1:5555`.
- `SECRET_KEY` random at runtime; `FLAG` is an env var. Admin superuser `palforge_admin` with default
  `ADMIN_PASSWORD=change-me-admin` (entrypoint uses `:-change-me-admin`).

## Admin access (confirmed)
`POST /api/auth/login/ {username:palforge_admin,password:change-me-admin}` → `role: admin`.
As admin, `GET /api/mods/` returns all mods incl. other users' (a previous solver's test mods:
`bz2.py`, `lzma.py`, `mimetypes.py` plants; nginx-conf / entrypoint / nginx-binary overwrites).

## Zip-slip write primitive
`upload_build_files` → `storage_dir = /data/media/builds/<mod_version>/<platform_code>`; each zip entry
written as `storage_dir / basename(entry)`. `mod_version` and `platform_code` are attacker-controlled
(max_length=20 each), so with `../..` the write can land at any writable path. Confirmed working:
- `/usr/share/nginx/html` (served back via `GET /hello.txt`).
- `/usr/local/lib/python3.11` (new files and overwriting `bz2.py`/`lzma.py`/`mimetypes.py` → 200).
- `/usr/lib/python3.11` (200 for new files).

Not writable: `/app` (500, chmod `a-w`), `/proc/sysrq-trigger` (500), `/etc/cron.d` via absolute target (500).
`/etc/nginx/conf.d` and `/usr/local/bin` were writable for a previous solver (saved `storage_path`).

## RCE attempts (all failed to capture flag)
- Stdlib fresh-import: planted `bz2/lzma/mimetypes/tempfile/uuid/crypt/cgi` markers in
  `/usr/local/lib/python3.11` and `/usr/lib/python3.11`, triggered BZIP2/LZMA zip uploads, media serve,
  large multipart. None fired → those modules are cached by the running interpreter.
- Restart: `/proc/sysrq-trigger` not writable; filling `/data` tmpfs killed the instance and it was
  recreated (payload lost), so no restart-based RCE landed.
- Schema/docs, mods/builds data contained no flag.

## Intended flag access
RCE via zip-slip → write a Python module the app imports freshly (or overwrite `/entrypoint.sh` and force
a restart that preserves the writable layer) → dump `$FLAG` to the nginx web root and read it.
