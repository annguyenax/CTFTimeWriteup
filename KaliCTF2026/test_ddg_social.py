import urllib.request
import urllib.parse
import json
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

queries = ['site:linkedin.com "Nader Khoury" Amman', 'site:instagram.com "nullvoyager1"', 'site:instagram.com "naderk_47"', 'site:reddit.com "nullvoyager1"']

for q in queries:
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, context=ctx)
        html = response.read().decode('utf-8', errors='ignore')
        snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
        if snippets:
            print(f"Results for {q}:")
            for s in snippets:
                print(s.replace('<b>','').replace('</b>','').strip())
        else:
            print(f"No results for {q}")
    except Exception as e:
        print(f"Error {q}: {e}")
