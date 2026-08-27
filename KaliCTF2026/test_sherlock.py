import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

sites = {
    "Twitter": "https://x.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Linktree": "https://linktr.ee/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "TikTok": "https://www.tiktok.com/@{}"
}

username = "nullvoyager1"
print(f"Searching for {username}...")
for site, url_tmpl in sites.items():
    url = url_tmpl.format(username)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        response = urllib.request.urlopen(req, context=ctx, timeout=5)
        if response.status == 200:
            print(f"[+] Found on {site}: {url}")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"[?] Error on {site}: {e.code}")
    except Exception as e:
        pass
