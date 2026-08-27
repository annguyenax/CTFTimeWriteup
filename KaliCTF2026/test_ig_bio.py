import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.instagram.com/nullvoyager1/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    response = urllib.request.urlopen(req, context=ctx, timeout=10)
    html = response.read().decode('utf-8', errors='ignore')
    match = re.search(r'<meta property="og:description" content="(.*?)"', html)
    if match:
        print("Instagram Bio:", match.group(1))
    else:
        print("No bio found in meta tag")
except Exception as e:
    print(f"Error accessing {url}: {e}")
