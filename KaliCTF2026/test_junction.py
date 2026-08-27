import urllib.request
import urllib.parse
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote('"The Junction Hall" Amman')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    html = response.read().decode('utf-8', errors='ignore')
    snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
    for s in snippets:
        print(s.replace('<b>','').replace('</b>','').strip())
except Exception as e:
    print(e)
