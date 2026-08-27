from bs4 import BeautifulSoup

with open('jea_news.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
    
article = soup.find('div', class_='NewsDetails') or soup.find('div', class_='news-details') or soup.body
text = article.get_text(separator='\n', strip=True) if article else ''
print("Text length:", len(text))
for line in text.split('\n'):
    if "فريق" in line or "15" in line or "149" in line:
        print(line.encode('utf-8', errors='ignore').decode('utf-8'))
