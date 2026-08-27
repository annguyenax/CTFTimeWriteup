#!/usr/bin/env python3
"""Independent pcapng analysis: find the frame carrying HTB{...} and dump context."""
import struct, sys

PATH = r"D:\download\CTFTimeWriteup\HTB-TryOut\ics\Shush Protocol\files\_work\ics_shush_protocol\traffic.pcapng"
data = open(PATH, "rb").read()

def pcap_blocks(blob):
    """classic pcap (the .pcapng file is actually classic pcap, magic 0xa1b2c3d4)"""
    magic = struct.unpack_from("<I", blob, 0)[0]
    assert magic == 0xA1B2C3D4, f"magic {magic:08x}"
    off = 24
    frame = 0
    while off + 16 <= len(blob):
        _s, _u, incl, _o = struct.unpack_from("<IIII", blob, off)
        off += 16
        yield frame + 1, blob[off : off + incl]
        off += incl
        frame += 1

def pcapng_blocks(blob):
    off = 0
    frame = 0
    while off + 12 <= len(blob):
        btype, blen = struct.unpack_from("<II", blob, off)
        body = blob[off + 8 : off + blen - 4]
        if btype == 0x00000006:  # EPB
            frame += 1
            iface, tshi, tslo, caplen, origlen = struct.unpack_from("<IIIII", body, 0)
            pkt = body[16 : 16 + caplen]
            yield frame, tshi * (1 << 32) + tslo, pkt
        elif btype == 0x00000003:  # SPB
            frame += 1
            caplen = struct.unpack_from("<I", body, 0)[0]
            pkt = body[4 : 4 + caplen]
            yield frame, 0, pkt
        off += blen

def tcp_payload(pkt):
    if len(pkt) < 34:
        return None
    if pkt[12:14] != b"\x08\x00":
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

FLAG = b"HTB{"
hits = 0
for frame, pkt in pcap_blocks(data):
    # raw scan on whole packet first
    if FLAG in pkt:
        hits += 1
        idx = pkt.index(FLAG)
        eth = pkt[12:14].hex() if len(pkt) >= 14 else "?"
        ipproto = pkt[23] if len(pkt) >= 24 else 0
        print(f"RAW-HIT frame={frame} caplen={len(pkt)} ethertype=0x{eth} ip_proto={ipproto} flag_at={idx}")
        print(f"  context: {pkt[max(0,idx-40):idx+90]!r}")
    t = tcp_payload(pkt)
    if t:
        sip, dip, sport, dport, payload = t
        if FLAG in payload:
            hits += 1
            idx = payload.index(FLAG)
            print(f"TCP-HIT frame={frame}")
            print(f"  {sip}:{sport} -> {dip}:{dport}  payload_len={len(payload)}")
            print(f"  first 16 bytes: {payload[:16].hex(' ')}")
            print(f"  MBAP: tid={struct.unpack_from('>H',payload,0)[0]} proto={struct.unpack_from('>H',payload,2)[0]} len={struct.unpack_from('>H',payload,4)[0]} uid={payload[6]} fc=0x{payload[7]:02x}")
            print(f"  FLAG at payload offset {idx}")
            print(f"  payload hex: {payload.hex(' ')}")
print(f"total flag hits: {hits}")
