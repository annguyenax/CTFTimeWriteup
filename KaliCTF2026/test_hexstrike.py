import urllib.request
import json

url = "http://192.168.77.138:8888/v1/health"
try:
    response = urllib.request.urlopen(url, timeout=5)
    print(response.read().decode('utf-8'))
except Exception as e:
    print(e)
