#!/usr/bin/env python3
# SIUUU Clicker — collect ALL 7 parts from ONE instance, decrypt AES-CTR
import requests, base64, json, sys, re, time
from Crypto.Cipher import AES

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://144.79.188.39:39989"

def decode_jwt(token):
    parts = token.split(".")
    if len(parts) < 2: return None
    padded = parts[1] + "=" * (-len(parts[1]) % 4)
    try: return json.loads(base64.urlsafe_b64decode(padded))
    except: return None

S = requests.Session()
S.get(BASE + "/", timeout=20)

parts = {}      # part_num -> ciphertext hex
key_hex = None
nonce_hex = None

print("[*] Clicking until all 7 parts collected...")
for i in range(1, 1001):
    try:
        r = S.post(BASE + "/api/click", timeout=20)
    except Exception as e:
        print(f"  [{i}] error: {e}, retrying in 2s...")
        time.sleep(2)
        try: r = S.post(BASE + "/api/click", timeout=20)
        except: continue

    for c in S.cookies:
        if c.name == "siuuu_jwt":
            p = decode_jwt(c.value)
            if p and p.get("typ") == "challenge-cookie":
                pn = p["part"]
                if pn not in parts:
                    parts[pn] = p["ciphertext"]
                    key_hex = p.get("key", key_hex)
                    nonce_hex = p.get("nonce", nonce_hex)
                    print(f"  [{i}] Part {pn}/{p['total']}: ct={p['ciphertext']} key={p.get('key')} nonce={p.get('nonce')}")
                    if len(parts) == p["total"]:
                        print(f"  [{i}] ALL {p['total']} PARTS COLLECTED!")
                        break
    else:
        if i % 200 == 0:
            print(f"  [{i}] have {len(parts)}/7: {sorted(parts.keys())}")
        continue
    break

if len(parts) < 7:
    print(f"[-] Only got {len(parts)}/7: {sorted(parts.keys())}. Run again on same instance.")
    sys.exit(1)

print(f"\n[*] key={key_hex} nonce={nonce_hex}")
print(f"[*] Parts: { {k: parts[k] for k in sorted(parts)} }")

key = bytes.fromhex(key_hex)
nonce = bytes.fromhex(nonce_hex)

# Approach A: each part ctr=0 (independent)
print("\n--- Approach A: each part ctr=0 ---")
decoded_a = {}
for pn in sorted(parts):
    ct = bytes.fromhex(parts[pn])
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=0)
    decoded_a[pn] = cipher.decrypt(ct)
    print(f"  Part {pn}: {decoded_a[pn]}")
flag_a = b"".join(decoded_a[i] for i in sorted(decoded_a))
print(f"  Combined: {flag_a}")

# Approach B: single stream ctr=0
print("\n--- Approach B: single stream ctr=0 ---")
combined = b"".join(bytes.fromhex(parts[i]) for i in sorted(parts))
cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=0)
flag_b = cipher.decrypt(combined)
print(f"  {flag_b}")

# Approach C: each part ctr=part-1
print("\n--- Approach C: each part ctr=part-1 ---")
decoded_c = {}
for pn in sorted(parts):
    ct = bytes.fromhex(parts[pn])
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=pn-1)
    decoded_c[pn] = cipher.decrypt(ct)
    print(f"  Part {pn}: {decoded_c[pn]}")
flag_c = b"".join(decoded_c[i] for i in sorted(decoded_c))
print(f"  Combined: {flag_c}")

# Search for flag in all approaches
for label, f in [("A", flag_a), ("B", flag_b), ("C", flag_c)]:
    m = re.search(rb"PTITCTF\{[^}]+\}", f)
    if m: print(f"\n[FLAG from {label}] {m.group().decode()}")
    # also check for readable ASCII
    readable = bytes(b if 32 <= b < 127 else ord('.') for b in f)
    print(f"  [{label} readable] {readable.decode()}")
