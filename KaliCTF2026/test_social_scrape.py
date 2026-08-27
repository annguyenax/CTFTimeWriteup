import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    "https://www.instagram.com/nullvoyager1/",
    "https://www.reddit.com/user/nullvoyager1",
    "https://www.twitch.tv/nullvoyager1",
    "https://www.pinterest.com/nullvoyager1/",
    "https://www.tiktok.com/@nullvoyager1"
]

neighborhoods = ['abdoun','shmeisani','weibdeh','dabouq','khalda','sweifieh','rabieh','abdali','marka','taj','sweileh','tla','kursi','amman', 'jabal']

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        response = urllib.request.urlopen(req, context=ctx, timeout=10)
        html = response.read().decode('utf-8', errors='ignore')
        print(f"--- Checked {url} ---")
        for n in neighborhoods:
            if n.lower() in html.lower():
                print(f"[!] FOUND NEIGHBORHOOD / KEYWORD in {url}: {n}")
    except Exception as e:
        print(f"Error accessing {url}: {e}")
