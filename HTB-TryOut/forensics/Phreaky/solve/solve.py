#!/usr/bin/env python3
"""Phreaky solver: parse pcap -> SMTP emails -> password + zip parts -> reassemble -> flag."""
import os, re, struct, sys, email, io, zipfile, base64, glob

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(os.path.dirname(BASE), "files", "_work")
PCAP = os.path.join(WORK, "phreaky.pcap")
EVID = os.path.join(BASE, "evidence")
os.makedirs(EVID, exist_ok=True)

def parse_pcap(path):
    """Yield (ts, payload) for IPv4/TCP packets carrying data."""
    with open(path, "rb") as f:
        gh = f.read(24)
        if gh[:4] == b"\xd4\xc3\xb2\xa1":
            endian = "<"
        elif gh[:4] == b"\xa1\xb2\xc3\xd4":
            endian = ">"
        else:
            raise SystemExit("bad pcap magic")
        linktype = struct.unpack(endian + "I", gh[20:24])[0]
        while True:
            hdr = f.read(16)
            if len(hdr) < 16:
                break
            ts_sec, ts_usec, incl, orig = struct.unpack(endian + "IIII", hdr)
            data = f.read(incl)
            if len(data) < incl:
                break
            ts = ts_sec + ts_usec / 1e6
            pkt = data
            if linktype == 1:  # ethernet
                if len(pkt) < 14:
                    continue
                eth_type = struct.unpack(">H", pkt[12:14])[0]
                pkt = pkt[14:]
                if eth_type == 0x8100:  # vlan
                    eth_type = struct.unpack(">H", pkt[2:4])[0]
                    pkt = pkt[4:]
                if eth_type != 0x0800:
                    continue
            elif linktype == 101:  # raw ip
                pass
            else:
                continue
            if len(pkt) < 20:
                continue
            ver_ihl = pkt[0]
            proto = pkt[9]
            if proto != 6:  # TCP only
                continue
            ihl = (ver_ihl & 0x0F) * 4
            tcp = pkt[ihl:]
            if len(tcp) < 20:
                continue
            sport, dport = struct.unpack(">HH", tcp[0:4])
            doff = (tcp[12] >> 4) * 4
            payload = tcp[doff:]
            yield ts, sport, dport, payload

def reassemble(streams):
    """streams: dict key->list of (ts, payload). Return list of conn payloads sorted."""
    conns = {}
    for ts, sport, dport, payload in streams:
        key = (sport, dport)
        conns.setdefault(key, []).append((ts, payload))
    out = {}
    for key, chunks in conns.items():
        chunks.sort()
        out[key] = b"".join(c for _, c in chunks)
    return out

def extract_emails(conn_data):
    """Pull raw email bytes between DATA and \\r\\n.\\r\\n"""
    emails = []
    for key, blob in conn_data.items():
        start = 0
        while True:
            i = blob.find(b"DATA\r\n", start)
            if i < 0:
                break
            body_start = i + len(b"DATA\r\n")
            j = blob.find(b"\r\n.\r\n", body_start)
            if j < 0:
                break
            emails.append(blob[body_start:j])
            start = j + 5
    return emails

def main():
    print("[*] parsing pcap")
    packets = list(parse_pcap(PCAP))
    print(f"[+] {len(packets)} tcp packets")
    conns = reassemble(packets)
    print(f"[+] {len(conns)} connections")
    smtp_conns = {k: v for k, v in conns.items() if 25 in k}
    print(f"[+] SMTP conns: {list(smtp_conns.keys())}")
    emails = extract_emails(smtp_conns)
    print(f"[+] {len(emails)} emails")
    for n, raw in enumerate(emails, 1):
        with open(os.path.join(EVID, f"email_{n:02d}.eml"), "wb") as f:
            f.write(raw)

    # parse each email
    parts = []
    for n, raw in enumerate(emails, 1):
        msg = email.message_from_bytes(raw)
        pwd = None
        zipdata = None
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain":
                body = part.get_payload(decode=True) or b""
                m = re.search(rb"Password:\s*(\S+)", body)
                if m:
                    pwd = m.group(1).decode()
            elif ct == "application/zip" or part.get_filename():
                zipdata = part.get_payload(decode=True)
        if zipdata is None:
            print(f"[!] email {n}: no zip attachment")
            continue
        zp = os.path.join(EVID, f"part_{n:02d}.zip")
        with open(zp, "wb") as f:
            f.write(zipdata)
        parts.append((n, zp, pwd))
        print(f"  email {n:02d}: pwd={pwd!r} zip={len(zipdata)}B")

    # extract each zip
    chunks = {}
    for n, zp, pwd in parts:
        z = zipfile.ZipFile(zp)
        name = z.namelist()[0]
        data = z.read(name, pwd=pwd.encode())
        chunks[n] = (name, data)
        print(f"  extracted {n:02d}: {name} {len(data)}B")
        with open(os.path.join(EVID, f"chunk_{n:02d}_{os.path.basename(name)}"), "wb") as f:
            f.write(data)

    # reassemble in numeric order
    final = b""
    for n in sorted(chunks):
        final += chunks[n][1]
    out = os.path.join(WORK, "reassembled.bin")
    with open(out, "wb") as f:
        f.write(final)
    print(f"[+] reassembled {len(final)} bytes -> {out}")
    print("[*] head:", final[:64])

if __name__ == "__main__":
    main()
