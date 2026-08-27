import sys
sys.path.insert(0, ".")
import palforge as pf

tok = pf.login(*pf.ADMIN)
print("logged in")

# Test write to /app: ver climbs to root, code=app
try:
    r = pf.write_to_path(tok, "/app", "ztest.txt", b"hello app", "../../../../..", "app")
    print("write /app status:", r.status_code)
    print(r.text[:400])
except Exception as e:
    print("ERR", repr(e))
