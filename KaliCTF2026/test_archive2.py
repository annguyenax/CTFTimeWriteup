import urllib.request
import urllib.parse
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://archive.is/search/?q=x.com%2Fnullvoyager1"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    html = response.read().decode('utf-8', errors='ignore')
    links = re.findall(r'<a href="(https://archive\.is/[^"]+)"', html)
    for l in set(links):
        print("Archived URL:", l)
except Exception as e:
    print(e)
