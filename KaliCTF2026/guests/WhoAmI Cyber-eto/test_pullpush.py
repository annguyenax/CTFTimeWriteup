import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

usernames = ["jabutaifeha", "j_abutaifeha", "JAbuTaifeha", "JulianAbuTaifeha", "Cyber-eto"]

for u in usernames:
    url = f"https://api.pullpush.io/reddit/search/submission/?author={u}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, context=ctx)
        data = json.loads(response.read().decode('utf-8'))
        if data.get('data'):
            print(f"Found posts for {u}:")
            for post in data['data']:
                print(post.get('title'), post.get('selftext'))
    except Exception as e:
        pass
