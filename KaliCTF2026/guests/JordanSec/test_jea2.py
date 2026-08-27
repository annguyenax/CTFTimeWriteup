import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.jea.org.jo/EN/NewsDetails/2324" # let's search for "149" across jea news
url = "https://jea.org.jo/AR/List/News"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    html = response.read().decode('utf-8')
    print("Fetched Arabic JEA news")
except Exception as e:
    print(e)
