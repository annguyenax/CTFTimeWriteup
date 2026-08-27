import re

with open('skyline-parser/assets/reference/r03.pdf', 'rb') as f:
    content = f.read().decode('utf-8', errors='ignore')
    
# Extract all alphanumeric strings longer than 4 chars
strings = re.findall(r'[A-Za-z0-9_-]{4,}', content)
# Just print a few or search for neighborhood names
neighborhoods = ['abdoun','shmeisani','jabal','weibdeh','dabouq','khalda','sweifieh','rabieh','abdali','marka','taj','hussein','sweileh','tla','kursi','amman']
for s in strings:
    if any(n in s.lower() for n in neighborhoods):
        print("Found:", s)
        
print("File size:", len(content))
