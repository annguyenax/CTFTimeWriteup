import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote("site:jea.org.jo 149")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    html = response.read().decode('utf-8', errors='ignore')
    import re
    urls = re.findall(r'<a class="result__url" href="([^"]+)">', html)
    print("Found URLs:", urls)
except Exception as e:
    print(e)
