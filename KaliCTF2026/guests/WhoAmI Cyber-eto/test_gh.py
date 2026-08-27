import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://api.github.com/users/jabutaifeha",
    "https://api.github.com/users/JAbuTaifeha",
    "https://api.github.com/users/JulianAbuTaifeha"
]

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, context=ctx)
        print(f"Found on Github: {url}")
        print(response.read().decode('utf-8'))
    except Exception as e:
        print(f"{url} -> {e}")
