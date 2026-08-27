import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.reddit.com/user/j_abutaifeha/about.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    print("Found j_abutaifeha!")
    print(response.read().decode('utf-8')[:200])
except Exception as e:
    print(e)
