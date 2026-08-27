from bs4 import BeautifulSoup
import re

with open('jea_news.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

text = soup.get_text(separator=' ', strip=True)
sentences = [s.strip() for s in text.split('. ')]
for s in sentences:
    if "فريق" in s or "15" in s or "149" in s:
        print(s.encode('utf-8', errors='ignore').decode('utf-8'))
