import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

users = ["jAbuTaifeha", "jabutaifeha", "JulianA", "j.abutaifeha", "j_abutaifeha", "juliana", "JAbuTaifeha"]

for u in users:
    url = f"https://www.reddit.com/user/{u}/about.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, context=ctx)
        data = json.loads(response.read().decode('utf-8'))
        print(f"User {u} found!")
    except Exception as e:
        pass
