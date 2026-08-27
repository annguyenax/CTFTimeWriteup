#!/usr/bin/env python3
import subprocess, time, os
# precise file contents for 4mCnFu.exe
fc='75c7be35750a7b58f966c0ab5e65784898338d5c712c6d43'
candidates={
  "exact_nonnl": b"4mCnFu.exe",
  "exact_nl": b"4mCnFu.exe\n",
  "exact_null": b"4mCnFu.exe\x00",
  "rawflagcontent": bytes.fromhex(fc),
  "ascii_hex": fc.encode(),
  "fullflag": b"PTITCTF{"+fc.encode()+b"}",
  "empty": b"",
  "slashpath": b".\\4mCnFu.exe",
}
for name, content in candidates.items():
    with open("4mCnFu.exe","wb") as f: f.write(content)
    p=subprocess.Popen(['live_chall_patched.exe'],stdout=subprocess.PIPE)
    try: o=p.communicate(timeout=3)[0]
    except subprocess.TimeoutExpired: p.kill(); o=b'(timeout)'
    is_msg = b'sealed' in o
    print(f"[{name}] {'MESSAGE!' if is_msg else 'decoy'}: {o!r}")
    time.sleep(0.05)
