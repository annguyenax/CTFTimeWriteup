import requests

url = "https://preview.redd.it/welcome-reddit-community-v0-psvs7gkg91gh1.jpeg"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    with open('welcome.jpeg', 'wb') as f:
        f.write(response.content)
    print("Success downloading image")
else:
    print(f"Failed with status code {response.status_code}")
