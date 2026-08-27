import urllib.request, urllib.parse, re
url = 'https://www.youtube.com/results?search_query=' + urllib.parse.quote('How roblox expects us to talk to each other')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    titles = re.findall(r'"title":\{"runs":\[\{"text":"(.*?)"\}\]', html)
    for t in list(dict.fromkeys(titles))[:10]:
        print(t.encode('ascii', 'ignore').decode('ascii'))
except Exception as e:
    print(e)
