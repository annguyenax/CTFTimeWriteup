import urllib.request
import urllib.parse
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://archive.is/search/?q=x.com%2Fnullvoyager1"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    html = response.read().decode('utf-8', errors='ignore')
    if "No results" in html:
        print("No results on archive.is")
    else:
        print("Found results on archive.is")
except Exception as e:
    print(e)
