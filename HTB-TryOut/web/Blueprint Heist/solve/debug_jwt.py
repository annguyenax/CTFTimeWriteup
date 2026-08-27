import base64, hmac, hashlib, json, urllib.request

base = "http://154.57.164.68:31206"
with urllib.request.urlopen(base + "/getToken") as r:
    user = r.read().decode().strip()
print("user", user)

h, p, s = user.split(".")

def pad(x):
    return x + "=" * (-len(x) % 4)

print("header", base64.urlsafe_b64decode(pad(h)))
print("payload", base64.urlsafe_b64decode(pad(p)))

secrets = [
    "IM_Sup3r_K3y_pl3ase_b3_c4r3ful?",
    "IM_Sup3r_K3y_pl3ase_b3_c4r3ful",
    "IM_Sup3r_K3y_pl3ase_b3_c4r3ful?\n",
    "IM_Sup3r_K3y_pl3ase_b3_c4r3ful?\r\n",
    "secret=IM_Sup3r_K3y_pl3ase_b3_c4r3ful?",
]
for sec in secrets:
    sig = hmac.new(sec.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    got = base64.urlsafe_b64encode(sig).rstrip(b"=").decode()
    ok = got == s
    print(f"Q: secret={sec!r} match? |+ {ok} got={got[:20]} exp={s[:20]} | -")
