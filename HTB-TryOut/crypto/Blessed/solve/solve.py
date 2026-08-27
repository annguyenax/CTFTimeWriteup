#!/usr/bin/env python3
"""Blessed (HTB TryOut, crypto, hard)

Rogue-key + cheat Σ-protocol by cracking the truncated P-256 EC-LCG.
Lattice recovery follows 7Rocky (challenge author): 6 leaked MSBs → 3
consecutive points → 7 polynomial equations → LLL.
"""
import json, os, re, socket, sys
from functools import reduce

import sympy as sp
from flint import fmpz_mat
from Crypto.PublicKey import ECC

from py_ecc.bls.ciphersuites import G2ProofOfPossession as bls
from py_ecc.bls.g2_primitives import G1_to_pubkey, pubkey_to_G1
from py_ecc.bls.point_compression import decompress_G1
from py_ecc.bls.typing import G1Compressed
from py_ecc.optimized_bls12_381.optimized_curve import (
    add, G1, multiply, neg, normalize, Z1,
)

P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
A = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
GX = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
GY = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
Gpt = ECC.EccPoint(GX, GY, curve="p256")


def on_curve(x, y):
    x %= P
    y %= P
    return (y * y - (x * x * x + A * x + B)) % P == 0


def crack_ec_lcg(values):
    u1, v1, u2, v2, u3, v3 = [int(x) for x in values]
    a1, b1, a2, b2, a3, b3 = sp.symbols("a1 b1 a2 b2 a3 b3")
    gens = (a1, b1, a2, b2, a3, b3)
    gx, gy = GX, GY
    ec1 = (v1 + b1) ** 2 - (u1 + a1) ** 3 - A * (u1 + a1) - B
    ec2 = (v2 + b2) ** 2 - (u2 + a2) ** 3 - A * (u2 + a2) - B
    ec3 = (v3 + b3) ** 2 - (u3 + a3) ** 3 - A * (u3 + a3) - B
    ec4 = ((u1 + a1) + (u2 + a2) + gx) * ((u2 + a2) - (u1 + a1)) ** 2 - ((v2 + b2) + (v1 + b1)) ** 2
    ec5 = ((u2 + a2) + (u3 + a3) + gx) * ((u3 + a3) - (u2 + a2)) ** 2 - ((v3 + b3) + (v2 + b2)) ** 2
    ec6 = (gy - (v1 + b1)) * ((u2 + a2) - (u1 + a1)) - ((v2 + b2) + (v1 + b1)) * ((u1 + a1) - gx)
    ec7 = (gy - (v2 + b2)) * ((u3 + a3) - (u2 + a2)) - ((v3 + b3) + (v2 + b2)) * ((u2 + a2) - gx)
    polys = [sp.Poly(sp.expand(e), *gens, modulus=P) for e in (ec1, ec2, ec3, ec4, ec5, ec6, ec7)]
    mons = set()
    for pol in polys:
        mons.update(pol.monoms())
    mons = sorted(mons, key=lambda t: (sum(t) == 0, t))
    coeff = []
    for pol in polys:
        d = pol.as_dict()
        coeff.append([int(d.get(m, 0)) % P for m in mons])
    n, m = 7, len(mons)
    rows = []
    for i in range(7):
        row = [0] * (7 + m)
        row[i] = P
        for j in range(m):
            row[7 + j] = coeff[i][j]
        rows.append(row)
    for j in range(m):
        row = [0] * (7 + m)
        row[7 + j] = (1 << 256) if j == m - 1 else 1
        rows.append(row)
    T = list(map(list, zip(*rows)))
    mat = fmpz_mat([[int(x) for x in row] for row in T])
    red = mat.lll()
    L = [[int(red[i, j]) for j in range(red.ncols())] for i in range(red.nrows())]
    for vec in L:
        small = [int(val) for val in vec if abs(val) < (1 << 33) and abs(val) != (1 << 256)]
        for da in small + [0]:
            for s in (1, -1):
                aa = s * da
                if abs(aa) >= (1 << 33):
                    continue
                x = (u1 + aa) % P
                for db in small + [0]:
                    for t in (1, -1):
                        bb = t * db
                        y = (v1 + bb) % P
                        if not on_curve(x, y):
                            continue
                        try:
                            W = ECC.EccPoint(x, y, curve="p256")
                        except ValueError:
                            continue
                        W2, W3 = W + Gpt, W + Gpt + Gpt
                        if (int(W2.x) >> 32) == (u2 >> 32) and (int(W2.y) >> 32) == (v2 >> 32) \
                           and (int(W3.x) >> 32) == (u3 >> 32) and (int(W3.y) >> 32) == (v3 >> 32):
                            return W3
    raise RuntimeError("EC-LCG recovery failed")


class IO:
    def __init__(self, host, port):
        self.s = socket.create_connection((host, port), timeout=60)
        self.s.settimeout(60)
        self.buf = b""

    def recv_until(self, needle):
        if isinstance(needle, str):
            needle = needle.encode()
        while needle not in self.buf:
            d = self.s.recv(4096)
            if not d:
                raise EOFError(self.buf[-400:].decode("latin1", "replace"))
            self.buf += d
        i = self.buf.index(needle) + len(needle)
        out, self.buf = self.buf[:i], self.buf[i:]
        return out

    def sendline(self, data):
        if isinstance(data, str):
            data = data.encode()
        if not data.endswith(b"\n"):
            data += b"\n"
        self.s.sendall(data)

    def sr(self, obj):
        self.recv_until(b"> ")
        self.sendline(json.dumps(obj))
        line = self.recv_until(b"\n").decode()
        return json.loads(line)


def g1_hex(pt):
    return bytes(G1_to_pubkey(pt)).hex()


def solve(host, port):
    io = IO(host, port)
    io.recv_until(b"> ")
    # first prompt already consumed conceptually — actually recv_until left empty after >
    # restore: we consumed "> ", good. But sr() also waits for "> ".
    # We already ate the first "> ", so send create directly then use sr for later.
    io.sendline(json.dumps({"cmd": "create"}))
    res = json.loads(io.recv_until(b"\n").decode())
    sk = int(res["sk"], 16)
    robot_id = int(res["robot_id"], 16)
    print("[*] created", res.get("msg"), "id", hex(robot_id)[:18])

    sig = bls.Sign(sk, b"list")
    io.recv_until(b"> ")
    io.sendline(json.dumps({"cmd": "list", "robot_id": hex(robot_id), "sig": sig.hex()}))
    robots = json.loads(io.recv_until(b"\n").decode())
    ids, Pks = [], []
    for r in robots:
        ids.append(int(r["robot_id"], 16))
        Pks.append(decompress_G1(G1Compressed(int(r["pk"], 16))))
    print("[*] listed", len(ids), "robots")

    t = 1337
    cmd = "unveil_secrets"
    pk = bls.SkToPk(t)
    sig_unv = bls.Sign(t, cmd.encode())
    Pk = pubkey_to_G1(pk)
    Pk_prime = add(Pk, neg(reduce(add, Pks, Z1)))
    pk_prime = G1_to_pubkey(Pk_prime)
    assert normalize(add(reduce(add, Pks), Pk_prime)) == normalize(Pk)
    print("[+] rogue key ready")

    io.recv_until(b"> ")
    io.sendline(json.dumps({"cmd": "join", "pk": pk_prime.hex()}))
    jres = json.loads(io.recv_until(b"\n").decode())
    rogue_id = int(jres["robot_id"], 16)
    ids.append(rogue_id)
    assert len(ids) == 6
    print("[*] joined rogue", hex(rogue_id)[:18])

    Wn = crack_ec_lcg([i << 32 for i in ids])
    print("[+] cracked EC-LCG", hex(int(Wn.x))[:18])

    io.recv_until(b"> ")
    io.sendline(json.dumps({"cmd": "verify", "robot_id": hex(rogue_id)}))
    # prove banner + first C prompt
    blob = io.recv_until(b"(hex): ")
    use_g1 = b"x * G1" in blob
    use_pk = b"x * pk" in blob or not use_g1
    print("[*] verify prompt G1" if use_g1 else "[*] verify prompt pk")

    for rnd in range(64):
        if rnd:
            io.recv_until(b"(hex): ")
        Wn_use = None
        # 64 coins = 32 points * 2 coords, starting at W_next = Wn+G
        # coin k uses (W_{n+1+k//2}).x if k even else .y
        if rnd % 2 == 0:
            Wn = Wn + Gpt
            coord = int(Wn.x)
        else:
            coord = int(Wn.y)
        coin = (coord >> 32) & 1
        if coin:
            x = int.from_bytes(os.urandom(16), "big")
            C = multiply(G1, x) if use_g1 else multiply(Pk_prime, x)
            io.sendline(g1_hex(C))
            io.recv_until(b"(hex): ")
            io.sendline(hex(x))
        else:
            sk_x = int.from_bytes(os.urandom(16), "big")
            C = add(multiply(G1, sk_x), neg(Pk_prime))
            io.sendline(g1_hex(C))
            io.recv_until(b"(hex): ")
            io.sendline(hex(sk_x))
        if rnd % 8 == 7:
            print("[*] zkp round", rnd + 1)

    # verified json
    rest = io.recv_until(b"> ")
    print("[*] after zkp", rest.decode("latin1", "replace")[:200].replace("\n", " "))
    io.sendline(json.dumps({"cmd": cmd, "sig": sig_unv.hex()}))
    line = io.recv_until(b"\n").decode()
    print("[*] unveil", line)
    m = re.search(r"HTB\{[^}]*\}", line)
    if not m:
        extra = io.buf.decode("latin1", "replace")
        print("[*] extra", extra[:400])
        m = re.search(r"HTB\{[^}]*\}", extra)
    if m:
        flag = m.group(0)
        open("final_flag.txt", "w").write(flag + "\n")
        print("FLAG:", flag)
        return flag
    return None


if __name__ == "__main__":
    h, p = (sys.argv[1], int(sys.argv[2])) if len(sys.argv) == 3 else ("154.57.164.65", 31465)
    solve(h, p)
