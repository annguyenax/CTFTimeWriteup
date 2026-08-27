import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

usernames = ["iAbuTaifeha", "IAbuTaifeha", "i_abutaifeha", "I_AbuTaifeha"]
for user in usernames:
    url = f"https://api.github.com/users/{user}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, context=ctx)
        data = json.loads(response.read().decode('utf-8'))
        print(f"Found on Github: {user}")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"Error {e.code} for {user}")
    except Exception as e:
        print(f"Error for {user}: {e}")
