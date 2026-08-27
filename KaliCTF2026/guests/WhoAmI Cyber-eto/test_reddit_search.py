import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.reddit.com/search.json?q=" + urllib.parse.quote("AbuTaifeha")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    data = json.loads(response.read().decode('utf-8'))
    for child in data['data']['children']:
        print(child['data']['title'])
        print("Author:", child['data']['author'])
        print(child['data']['selftext'][:200])
except Exception as e:
    print(e)
