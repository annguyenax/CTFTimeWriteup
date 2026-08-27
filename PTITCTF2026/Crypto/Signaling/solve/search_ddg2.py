import urllib.request, urllib.parse, re
url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote('Roblox Semaphore emote spells')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    titles = re.findall(r'class="result__snippet[^>]*>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)
    for t in list(dict.fromkeys(titles))[:10]:
        print(re.sub('<[^<]+>', '', t).strip())
except Exception as e:
    print(e)
