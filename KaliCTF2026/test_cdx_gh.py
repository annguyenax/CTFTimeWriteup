import urllib.request
import urllib.parse
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://web.archive.org/cdx/search/cdx?url=github.com/nullvoyager1*&output=json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    data = response.read().decode('utf-8', errors='ignore')
    print("CDX Output for GitHub:", data)
except Exception as e:
    print(e)
