import requests

s = requests.Session()
r_login = s.post('http://144.79.188.36:6500/api/session', json={'username': 'luongvd', 'password': 'luongvd'})
print('Login:', r_login.status_code)

for i in range(0, 25):
    try:
        r = s.get(f'http://144.79.188.36:6500/api/images/{i}', timeout=5)
        print(f"ID {i:2d}: HTTP {r.status_code} | Size: {len(r.content):6d} bytes")
    except Exception as e:
        print(f"ID {i:2d}: Error {e}")
