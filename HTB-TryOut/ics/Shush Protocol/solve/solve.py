#!/usr/bin/env python3
"""Shush Protocol — extract HTB{...} from Modbus/TCP function 0x66 in the pcap."""
from __future__ import annotations

import argparse
import re
import struct
import sys
import zipfile
from pathlib import Path

FLAG_RE = re.compile(rb"HTB\{[^}]+\}")


def iter_pcap_frames(blob: bytes):
    magic, vmaj, vmin, _zone, _sig, _snap, network = struct.unpack_from("<IHHIIII", blob, 0)
    if magic != 0xA1B2C3D4:
        raise SystemExit(f"unexpected pcap magic {magic:08x}")
    off = 24
    n = 0
    while off + 16 <= len(blob):
        ts_sec, ts_usec, incl, orig = struct.unpack_from("<IIII", blob, off)
        off += 16
        pkt = blob[off : off + incl]
        off += incl
        n += 1
        yield n, ts_sec, ts_usec, network, pkt


def tcp_payload(pkt: bytes) -> tuple[str, str, int, int, bytes] | None:
    if len(pkt) < 34:
        return None
    if struct.unpack_from(">H", pkt, 12)[0] != 0x0800:
        return None
    ihl = (pkt[14] & 0xF) * 4
    if pkt[23] != 6:
        return None
    sip = ".".join(map(str, pkt[26:30]))
    dip = ".".join(map(str, pkt[30:34]))
    l4 = 14 + ihl
    if len(pkt) < l4 + 20:
        return None
    sport, dport = struct.unpack_from(">HH", pkt, l4)
    doff = (pkt[l4 + 12] >> 4) * 4
    return sip, dip, sport, dport, pkt[l4 + doff :]


def parse_modbus(payload: bytes) -> dict | None:
    if len(payload) < 8:
        return None
    tid, proto, length, uid, func = struct.unpack_from(">HHHBB", payload, 0)
    if proto != 0:
        return None
    return {
        "tid": tid,
        "proto": proto,
        "length": length,
        "uid": uid,
        "func": func,
        "data": payload[8:],
    }


def extract_flag(pcap: bytes) -> tuple[str, int, dict]:
    for n, _s, _u, _net, pkt in iter_pcap_frames(pcap):
        t = tcp_payload(pkt)
        if not t:
            continue
        sip, dip, sport, dport, payload = t
        if 502 not in (sport, dport):
            continue
        mb = parse_modbus(payload)
        if not mb:
            continue
        m = FLAG_RE.search(mb["data"]) or FLAG_RE.search(payload)
        if m:
            info = {
                "frame": n,
                "src": f"{sip}:{sport}",
                "dst": f"{dip}:{dport}",
                "func": mb["func"],
                "tid": mb["tid"],
            }
            return m.group(0).decode(), n, info
    raise SystemExit("no HTB{...} in Modbus/TCP payloads")


def load_pcap(path: Path) -> bytes:
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if n.endswith((".pcap", ".pcapng")) and not n.startswith("__")]
            if not names:
                raise SystemExit("no pcap in zip")
            return z.read(names[0])
    return path.read_bytes()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--zip",
        default=str(
            Path(__file__).resolve().parents[1] / "files" / "ics_shush_protocol.zip"
        ),
    )
    args = p.parse_args()
    blob = load_pcap(Path(args.zip))
    flag, frame, info = extract_flag(blob)
    ev = Path(__file__).resolve().parent / "evidence"
    ev.mkdir(parents=True, exist_ok=True)
    (ev / "01_modbus_flag.txt").write_text(
        f"Q: which Modbus frame carries the secret?\n"
        f"frame={frame} {info['src']} -> {info['dst']} FC=0x{info['func']:02x} TID={info['tid']}\n"
        f"FLAG={flag}\n",
        encoding="utf-8",
    )
    print(flag)
    return 0


if __name__ == "__main__":
    sys.exit(main())
