#!/usr/bin/env python3
import subprocess, time, shutil, os
fc='75c7be35750a7b58f966c0ab5e65784898338d5c712c6d43'
candidates = {
  "raw_bytes": bytes.fromhex(fc),
  "ascii_hex": fc.encode(),
  "fullflag": b"PTITCTF{"+fc.encode()+b"}",
  "hex_with_newline": fc.encode()+b"\n",
  "4mCnFu.exe": b"4mCnFu.exe",
}
# put ping as 4mCnFu.exe in a temp dir (process detection)
os.makedirs("tmpproc", exist_ok=True)
shutil.copy(r"C:\Windows\System32\ping.exe", "tmpproc\\4mCnFu.exe")
for name, content in candidates.items():
    with open("4mCnFu.exe","wb") as f: f.write(content)
    pp=subprocess.Popen(["tmpproc\\4mCnFu.exe","-t","127.0.0.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.25)
    p=subprocess.Popen(["live_chall_p3.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.8)
    out=p.stdout.read() if p.stdout else b''
    p.kill(); pp.terminate()
    print(f"[file={name}] out={out!r}")
    time.sleep(0.1)
