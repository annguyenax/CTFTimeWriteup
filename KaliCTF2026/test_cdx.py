import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://web.archive.org/cdx/search/cdx?url=twitter.com/nullvoyager1*&output=json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    print(response.read().decode('utf-8'))
except Exception as e:
    print(e)

url2 = "https://web.archive.org/cdx/search/cdx?url=x.com/nullvoyager1*&output=json"
req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req2, context=ctx)
    print(response.read().decode('utf-8'))
except Exception as e:
    print(e)
