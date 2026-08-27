#!/usr/bin/env python3
# SIUUU Clicker — auto-click 1000 times, collect challenge-cookie JWTs
import requests, base64, json, sys

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://144.79.188.39:39957"
S = requests.Session()

# Initial GET
S.get(BASE + "/", timeout=10)

challenge_jwts = []

def decode_jwt(token):
    parts = token.split(".")
    if len(parts) < 2:
        return None
    padded = parts[1] + "=" * (-len(parts[1]) % 4)
    try:
        return json.loads(base64.urlsafe_b64decode(padded))
    except Exception:
        return None

for i in range(1, 1001):
    r = S.post(BASE + "/api/click", timeout=10)
    data = r.json()
    
    # Check all cookies for challenge JWTs
    jwt_val = None
    for c in S.cookies:
        if c.name == "siuuu_jwt":
            jwt_val = c.value
    
    if jwt_val:
        payload = decode_jwt(jwt_val)
        if payload and payload.get("typ") == "challenge-cookie":
            challenge_jwts.append(payload)
            print(f"[{i}] CHALLENGE JWT: {json.dumps(payload, indent=2)}")
    
    if i % 100 == 0:
        print(f"[{i}] count={data.get('count')}, cookies: {[c.name for c in S.cookies]}")
    
    if data.get("finished"):
        print(f"[{i}] FINISHED! fake_flag={data.get('fake_flag')}")
        # Check final cookies
        for c in S.cookies:
            if c.name == "siuuu_jwt":
                p = decode_jwt(c.value)
                print(f"  Final JWT: {json.dumps(p, indent=2)}")

print(f"\n=== Collected {len(challenge_jwts)} challenge JWTs ===")
for j in challenge_jwts:
    print(json.dumps(j))

# Also decode ALL current cookies
print("\n=== Final cookie state ===")
for c in S.cookies:
    print(f"  {c.name} = {c.value[:80]}...")
    if c.name == "siuuu_jwt":
        p = decode_jwt(c.value)
        print(f"  -> {json.dumps(p, indent=2)}")
