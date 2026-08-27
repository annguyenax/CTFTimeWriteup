import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://api.github.com/search/issues?q=nullvoyager1"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    issues = json.loads(response.read().decode('utf-8'))
    print(json.dumps(issues, indent=2))
except Exception as e:
    print(e)
