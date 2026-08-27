import urllib.request, urllib.parse, bs4
url = 'https://www.google.com/search?q=' + urllib.parse.quote('"How roblox expects us to talk to each other"')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for p in soup.find_all(['h3', 'div']):
        text = p.get_text(strip=True)
        if "roblox" in text.lower():
            print(text.encode('ascii', 'ignore').decode('ascii'))
except Exception as e:
    print(e)
