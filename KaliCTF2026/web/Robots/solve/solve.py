#!/usr/bin/env python3
import requests
import re
import sys

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://f1a4.chall.kali-team.online:8001/robots.txt"
        
    headers = {"User-Agent": "Googlebot"}
    r = requests.get(url, headers=headers)
    
    match = re.search(r'KaliTeam\{[^}]+\}', r.text)
    if match:
        print("Flag found:", match.group(0))
    else:
        print("Flag not found.")

if __name__ == '__main__':
    main()
