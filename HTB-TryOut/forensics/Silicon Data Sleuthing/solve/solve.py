#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Silicon Data Sleuthing (HTB TryOut, forensics, easy) — end-to-end solver
========================================================================
The terminal service (nc) asks 8 questions about the OpenWrt firmware dump
`chal_router_dump.bin`; answering all 8 prints the flag. The flag's hash suffix
is PER-INSTANCE, so we recompute the answers from the dump and drive the quiz.

Firmware layout (16 MiB flash):
  0x180000  uImage kernel
  0x42c2c8  squashfs (xz)  -> read-only rootfs  (OpenWrt 23.05.0, kernel 5.15.134)
  overlay   JFFS2 (rootfs_data) — nodetypes 0xe001 dirent / 0xe002 inode; the
            interesting /etc/* files are LZMA (compr 8) with raw-LZMA1 params
            lc=0 lp=0 pb=0, dict 0x10000. Zero-length nodes are metadata-only.

Answers recovered from the overlay:
  version 23.05.0 | kernel 5.15.134 | root shadow line ($1$...) |
  PPPoE user/pass (/etc/config/network) | WiFi SSID/key (/etc/config/wireless) |
  3 DNAT src_dport on WAN (/etc/config/firewall).

Usage: python solve.py [HOST PORT] [path/to/chal_router_dump.bin]
"""
import socket, re, time, struct, lzma, zlib, sys, os

DUMP = sys.argv[3] if len(sys.argv) > 3 else os.path.join(
    os.path.dirname(__file__), "..", "files", "_work", "chal_router_dump.bin")

# ---------- JFFS2 overlay extraction ----------
def dec(compr, pl, ds):
    if compr == 0: return pl[:ds]
    if compr == 6:
        try: return zlib.decompress(pl)[:ds]
        except Exception: return b""
    if compr == 8:  # OpenWrt JFFS2 LZMA (raw LZMA1, lc=0 lp=0 pb=0, dict 0x10000)
        hdr = bytes([0]) + struct.pack("<I", 0x10000) + struct.pack("<Q", ds)
        try: return lzma.decompress(hdr + pl, format=lzma.FORMAT_ALONE)[:ds]
        except Exception: return b""
    return pl

def parse_overlay(data):
    dirents, inodes = {}, {}
    pos, n = 0, len(data)
    while pos + 12 <= n:
        if data[pos:pos+2] != b"\x85\x19":
            pos += 4; continue
        nt = struct.unpack_from("<H", data, pos+2)[0]
        tl = struct.unpack_from("<I", data, pos+4)[0]
        if tl < 12 or tl > 0x10000 or pos+tl > n:
            pos += 4; continue
        if nt == 0xe001:  # dirent
            pino, ver, ino, _ = struct.unpack_from("<IIII", data, pos+12)
            ns, typ = data[pos+28], data[pos+29]
            name = data[pos+40:pos+40+ns]
            k = (pino, name)
            if k not in dirents or ver > dirents[k][0]:
                dirents[k] = (ver, ino, typ)
        elif nt == 0xe002:  # inode
            ino, ver = struct.unpack_from("<II", data, pos+12)
            isize = struct.unpack_from("<I", data, pos+28)[0]
            off, cs, ds = struct.unpack_from("<III", data, pos+44)
            compr = data[pos+56]
            inodes.setdefault(ino, []).append((ver, off, cs, ds, compr, isize,
                                               data[pos+68:pos+68+cs]))
        pos += (tl + 3) & ~3
    return dirents, inodes

def cat(inodes, ino):
    frags, fsize = {}, 0
    for ver, off, cs, ds, compr, isize, pl in sorted(inodes.get(ino, [])):
        fsize = isize
        if ds == 0 or cs == 0:          # metadata-only node, skip
            continue
        frags[off] = dec(compr, pl, ds)
    out = bytearray()
    for off in sorted(frags):
        if off > len(out): out += b"\x00" * (off - len(out))
        out[off:off+len(frags[off])] = frags[off]
    return bytes(out[:fsize] if fsize else out)

def ino_of(dirents, name):
    for (pino, nm), (ver, ino, typ) in dirents.items():
        if nm == name: return ino
    return None

def recover_answers(dump):
    data = open(dump, "rb").read()
    dirents, inodes = parse_overlay(data)
    def cfg(name): return cat(inodes, ino_of(dirents, name)).decode("latin1", "replace")
    shadow  = cat(inodes, ino_of(dirents, b"shadow")).decode("latin1", "replace")
    net, wifi, fw = cfg(b"network"), cfg(b"wireless"), cfg(b"firewall")
    root_line = next(l for l in shadow.splitlines() if l.startswith("root:"))
    def opt(txt, key):
        m = re.search(r"option %s '([^']*)'" % key, txt); return m.group(1) if m else None
    ports = sorted(int(m) for m in re.findall(r"option src_dport '(\d+)'", fw))
    return {
        "version": "23.05.0", "kernel": "5.15.134", "shadow": root_line,
        "pppoe_user": opt(net, "username"), "pppoe_pass": opt(net, "password"),
        "ssid": opt(wifi, "ssid"), "wifi_key": opt(wifi, "key"),
        "ports": ",".join(map(str, ports)),
    }

# ---------- quiz driver ----------
ANSI = re.compile(r"\x1b\[[0-9;]*m")
def run_quiz(host, port, ans):
    rules = [
        (r"version of openwrt|openwrt.*run", ans["version"]),
        (r"kernel", ans["kernel"]),
        (r"root account|hash of the root|shadow", ans["shadow"]),
        (r"pppoe.*user", ans["pppoe_user"]),
        (r"pppoe.*pass", ans["pppoe_pass"]),
        (r"ssid|wifi.*name|network name", ans["ssid"]),
        (r"wifi.*(pass|key)|wireless.*(pass|key)|passphrase", ans["wifi_key"]),
        (r"redirect|wan ports|dnat", ans["ports"]),
    ]
    pick = lambda q: next((a for p, a in rules if re.search(p, q.lower())), None)
    s = socket.create_connection((host, port), timeout=12); s.settimeout(8)
    def read():
        buf = b""
        try:
            while True:
                d = s.recv(4096)
                if not d: break
                buf += d
                t = ANSI.sub("", buf.decode("latin1", "replace"))
                if t.rstrip().endswith(">") or "HTB{" in t: break
        except socket.timeout: pass
        return ANSI.sub("", buf.decode("latin1", "replace"))
    def question(t):
        L = [l.strip() for l in t.splitlines() if l.strip() and l.strip() != ">"
             and not set(l.strip()) <= set(">+-| ")]
        c = [l for l in L if l.endswith("?") or "(ex:" in l or "sperated" in l
             or (l.split() and l.split()[0] in ("What", "Which", "How", "Enter", "Name"))]
        return (c[-1] if c else (L[-1] if L else t))
    full = []
    for _ in range(25):
        t = read(); full.append(t)
        if "HTB{" in t: break
        a = pick(question(t))
        if a is None:
            print("UNKNOWN QUESTION:\n", t[-400:]); break
        s.sendall(a.encode() + b"\n"); time.sleep(0.4)
    m = re.search(r"HTB\{[^}]*\}", "".join(full))
    return m.group(0) if m else None

if __name__ == "__main__":
    ans = recover_answers(DUMP)
    print("[*] recovered answers:")
    for k, v in ans.items(): print("    %-11s %s" % (k, v))
    host, port = (sys.argv[1], int(sys.argv[2])) if len(sys.argv) >= 3 else ("154.57.164.82", 32170)
    print("[*] driving quiz on %s:%d ..." % (host, port))
    flag = run_quiz(host, port, ans)
    if flag:
        open(os.path.join(os.path.dirname(__file__), "..", "final_flag.txt"), "w").write(flag + "\n")
        print("[+] FLAG:", flag)
    else:
        print("[-] no flag (instance down or question set changed)")
