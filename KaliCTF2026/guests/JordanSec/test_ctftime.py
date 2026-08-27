import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://ctftime.org/stats/JO"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    html = response.read().decode('utf-8')
    teams = re.findall(r'<a href="/team/\d+">([^<]+)</a>', html)
    print("Teams in Jordan:", teams[:30])
except Exception as e:
    print(e)
