#!/usr/bin/env python3
r"""
Transcendent Renovation (L3akCTF 2026 - Beginner/forensics) analyzer.

The challenge ships Windows Jump Lists (AutomaticDestinations / CustomDestinations)
and a ncat --ssl "Ghost Hunt Terminal" that asks 7 questions about the folder
`NoNeedToWonder`. This script extracts the answers from the Jump List.

Prereq:  pip install olefile
Usage:   python solve.py <AutomaticDestinations dir>   # dir with *.automaticDestinations-ms
         (or point directly at f01b4d95cf55d32a.automaticDestinations-ms)

Answers (6/7 verified accepted by the live service):
  Q1 file format ............ OLE CF            (`file` says "Composite Document File V2")
  Q2 automaticDestinations ... f01b4d95cf55d32a.automaticDestinations-ms
  Q3 share path ............. \\tsclient\HauntedHouse   (RDP redirected drive)
  Q4 stream (rename data) ... 46                (DestList entry -> stream 0x46)
  Q5 File Droid GUID ........ ec2ab952-7e4d-11f1-89ad-a2dead7852ad  (lowercase, no braces)
  Q6 hostname ............... logging-vm        (LNK TrackerDataBlock MachineID)
  Q7 original name .......... SoulSearch (forensic) -- REJECTED by service (unresolved)
"""
import sys, os, struct, re
import olefile

def guid(b):
    d1, d2, d3 = struct.unpack('<IHH', b[:8]); d4 = b[8:16]
    return "%08x-%04x-%04x-%s-%s" % (d1, d2, d3, d4[:2].hex(), d4[2:].hex())

def find_file(arg):
    if os.path.isdir(arg):
        for f in os.listdir(arg):
            if f.endswith("automaticDestinations-ms"):
                d = open(os.path.join(arg, f), "rb").read()
                if b"N\x00o\x00N\x00e\x00e\x00d" in d or b"NoNeedToWonder" in d:
                    return os.path.join(arg, f), f
        raise SystemExit("No automaticDestinations file with NoNeedToWonder found")
    return arg, os.path.basename(arg)

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "."
    path, name = find_file(arg)
    print("Q1 file format : OLE CF  (Composite Document File V2)")
    print("Q2 auto file   :", name)

    ole = olefile.OleFileIO(path)

    # DestList: locate the NoNeedToWonder entry -> its stream number (Q4)
    dl = ole.openstream('DestList').read()
    ver, nent = struct.unpack('<2I', dl[:8]); off = 32; stream_hex = None
    for _ in range(nent):
        if off + 0x82 > len(dl): break
        nchar = struct.unpack('<H', dl[off+0x80:off+0x82])[0]
        pathstr = dl[off+0x82:off+0x82+nchar*2].decode('utf-16-le', 'replace')
        stream = struct.unpack('<I', dl[off+0x58:off+0x5c])[0]
        if pathstr.endswith("NoNeedToWonder"):
            stream_hex = "%x" % stream
        off += 0x82 + nchar*2 + 4
    print("Q4 stream      :", stream_hex)

    data = ole.openstream(stream_hex).read()

    # Q3 share path (UNC) anywhere in the file (it lives in the tsclient share entry)
    share = None
    for entry in ole.listdir():
        blob = ole.openstream(entry).read()
        mm = re.search(rb'\\\\[\x20-\x5b\x5d-\x7e]{3,}\\[\x20-\x5b\x5d-\x7e]{3,}', blob)
        if mm:
            share = mm.group().decode('latin1'); break
    print("Q3 share path  :", share)

    # Q5/Q6 from the LNK TrackerDataBlock (sig 0xA0000003)
    i = data.find(b'\x03\x00\x00\xa0')
    if i >= 4:
        blk = data[i-4:]
        machine = blk[16:32].split(b'\x00')[0].decode('latin1', 'replace')
        droidfile = blk[48:64]
        print("Q6 hostname    :", machine)
        print("Q5 File Droid  :", guid(droidfile))

    # names present in the stream: current (LNK proper) + remnant (previous)
    names = [m.group().decode('utf-16-le') for m in
             re.finditer(rb'(?:[\x20-\x7e]\x00){4,}', data)]
    folders = [n for n in names if n in ("NoNeedToWonder", "SoulSearch")]
    print("Q7 names in stream (current + rename remnant):", folders)
    print("   -> forensic original name = SoulSearch  (rejected by service; unresolved)")
    ole.close()

if __name__ == "__main__":
    main()
