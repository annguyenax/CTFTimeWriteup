#!/usr/bin/env python3
"""
PTITCTF 2026 - Crypto: "CIA - What does 'I' stand for?"

Concept: 'I' in the CIA triad = INTEGRITY. The outermost ZIP password is
    sha256(FLAG).hexdigest(), so the flag is the unique string whose SHA-256
    equals the recovered password (an integrity/hash check).

Layers (all RSA moduli are 280-bit = two 140-bit primes -> factorable):
  0) chall.zip    password = sha256(flag)            (4 x 280-bit segments)
  1) secret.zip   password = RSA(secret.py, 1 chunk) (random 32-hex password)
  2) flag.zip     password = RSA(flag.py,   1 chunk)
     -> flag.txt  = DECOY  PTITCTF{y0Ur_3ff0r7_...}   (violates the hash)
The REAL flag is assembled from sub-challenges inside chall.zip:
   chall3 (RSA batch-gcd, 2 messages)  +  chall6 (Hastad e=3)  +  chall7 (Rabin),
each plaintext being a hex string that decodes to a REVERSED fragment.
"""

import os, re, io, glob, hashlib, zipfile, ast
from math import gcd
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long
import gmpy2

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP_PATH = os.path.join(BASE, "files", "chall.zip")
E = 65537

# Outer layer: 4 x 280-bit RSA segments -> 16-byte chunks of sha256(flag).
SEGMENTS = [
    {'n': 888523645462482914511937993639971675683449104268887971359610120913606538106474654137,
     'c': 796660109938607373103428634499485839198653250296503054132344525062218332871020114483},
    {'n': 1366132309756057281105160218268861952479185203873435489801392136075416106320399853767,
     'c': 396647050003890156872343276869733256818182173276169668090320320618210171160430729074},
    {'n': 749561422591023768140445791169825310368781851125173258987501126514210498901160658107,
     'c': 427075894942682511224493597089449453250756517080377694957651573884248784993336053454},
    {'n': 1189948736727152080936253296281529159687295527287026749817519351035173385872051118993,
     'c': 32979145778284568421482442582791679140913394890750234645498714210821084239237597797},
]
# Known factors (280-bit modulus = two 140-bit primes).
FACTORS = {
    888523645462482914511937993639971675683449104268887971359610120913606538106474654137:
        (816038443286324146051749864697465935484847, 1088825719881833826874734770997970677090071),
    1366132309756057281105160218268861952479185203873435489801392136075416106320399853767:
        (1096134935962049816277643537216664923557871, 1246317642961573541737717408379320425028777),
    749561422591023768140445791169825310368781851125173258987501126514210498901160658107:
        (790643357812107280431894889727685284754859, 948039865490343569959398817969461165882673),
    1189948736727152080936253296281529159687295527287026749817519351035173385872051118993:
        (991405450807867692135161548464024686216719, 1200264468747369902613990913429268593482847),
}


def decrypt_rsa(seg):
    n, c = seg['n'], seg['c']
    p, q = FACTORS[n]
    d = inverse(E, (p - 1) * (q - 1))
    return long_to_bytes(pow(c, d, n))


def getval(src, name):
    for line in src.splitlines():
        line = line.strip()
        if line.startswith(name + ' = '):
            return line.split('=', 1)[1].strip()
    return None


def solve_chall3(src):
    mods = ast.literal_eval(getval(src, 'MODULI'))
    e = int(getval(src, 'e'))
    cts = ast.literal_eval(getval(src, 'CIPHERTEXTS'))
    out = {}
    for item in cts:
        idx, c = item['modulus_index'], item['c']
        for other in mods:
            g = gcd(mods[idx], other)
            if g > 1 and g != mods[idx]:
                q = mods[idx] // g
                d = inverse(e, (g - 1) * (q - 1))
                m = long_to_bytes(pow(c, d, mods[idx]))
                out[idx] = bytes.fromhex(m.decode('latin1')).decode('latin1')[::-1]
                break
    return out[0], out[3]   # pieces start with "PTITCTF{..." and "...n736r1"


def solve_chall6(src):
    mods = ast.literal_eval(getval(src, 'MODULI'))
    cts = ast.literal_eval(getval(src, 'CIPHERTEXTS'))
    N = 1
    for m in mods:
        N *= m
    C = 0
    for m, c in zip(mods, cts):
        Mi = N // m
        C += c * Mi * inverse(Mi, m)
    C %= N
    m, _ = gmpy2.iroot(C, 3)          # Hastad broadcast, e = 3
    raw = long_to_bytes(int(m))
    return bytes.fromhex(raw.decode('latin1')).decode('latin1')[::-1]


def solve_chall7(src):
    p = int(getval(src, 'p')); q = int(getval(src, 'q')); c = int(getval(src, 'c'))
    n = p * q
    mp = pow(c, (p + 1) // 4, p)
    mq = pow(c, (q + 1) // 4, q)
    _, yp, yq = gmpy2.gcdext(p, q)
    yp, yq = int(yp), int(yq)
    for r in [(yp * p * mq + yq * q * mp) % n,
              n - ((yp * p * mq + yq * q * mp) % n),
              (yp * p * mq - yq * q * mp) % n,
              n - ((yp * p * mq - yq * q * mp) % n)]:
        b = long_to_bytes(r)
        if all(32 <= x < 127 for x in b):
            try:
                return bytes.fromhex(b.decode('latin1')).decode('latin1')[::-1]
            except Exception:
                pass
    raise RuntimeError("chall7 failed")


def main():
    # Layer 0: recover password = sha256(flag)
    password = b"".join(decrypt_rsa(s) for s in SEGMENTS).decode('ascii')
    print(f"[+] Layer-0 password (sha256 of FLAG): {password}")

    # Unpack chall.zip
    with zipfile.ZipFile(ZIP_PATH) as z:
        files = {nm: z.read(nm, pwd=password.encode('ascii')).decode()
                 for nm in z.namelist() if nm.endswith('.py') and nm != 'secret.py'}

    # Solve the 3 flag-bearing sub-challenges
    p1, p2 = solve_chall3(files['chall3.py'])
    p3 = solve_chall6(files['chall6.py'])
    p4 = solve_chall7(files['chall7.py'])
    print(f"    chall3[0]: {p1}")
    print(f"    chall3[3]: {p2}")
    print(f"    chall6   : {p3}")
    print(f"    chall7   : {p4}")

    flag = p1 + p2 + p3 + p4
    print(f"\n[+] Flag: {flag}")

    # Integrity verification: sha256(flag) must equal the ZIP password
    h = hashlib.sha256(flag.encode()).hexdigest()
    print(f"[*] sha256(flag) = {h}")
    assert h == password, "INTEGRITY CHECK FAILED"
    print("[+] INTEGRITY VERIFIED  (CIA 'I' satisfied)")

    with open(os.path.join(BASE, "final_flag.txt"), "w") as f:
        f.write(flag + "\n")


if __name__ == "__main__":
    main()
