import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://preview.redd.it/welcome-reddit-community-v0-psvs7gkg91gh1.jpeg?auto=webp&s=cb80d9ebdf0f2dc2009219e9efc99ceb3637e199"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req, context=ctx)
    with open('welcome.jpg', 'wb') as f:
        f.write(response.read())
    print("Downloaded welcome.jpg")
except Exception as e:
    print(e)
