import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://api.pullpush.io/reddit/search/submission/?author=J_AbuTaifeha"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    data = json.loads(response.read().decode('utf-8'))
    if data.get('data'):
        print(f"Found posts for J_AbuTaifeha:")
        for post in data['data']:
            print("Title:", post.get('title'))
            print("Text:", post.get('selftext'))
    else:
        print("No posts found in archive.")
except Exception as e:
    print(e)
