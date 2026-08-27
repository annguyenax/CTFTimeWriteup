import os
import re

repo_path = 'skyline-parser'
for root, dirs, files in os.walk(repo_path):
    if '.git' in root:
        continue
    for file in files:
        if file.endswith(('.txt', '.csv', '.log', '.md', '.py')):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if 'amman' in content.lower() or 'location' in content.lower():
                    print(f"File {filepath} contains 'amman' or 'location'")
                # Print all unique words starting with a capital letter that might be a place
                words = re.findall(r'\b[A-Z][a-z]+\b', content)
                for w in set(words):
                    if w in ['Abdoun', 'Shmeisani', 'Jabal', 'Weibdeh', 'Dabouq', 'Khalda', 'Sweifieh', 'Rabieh', 'Abdali', 'Marka', 'Taj', 'Hussein', 'Sweileh', 'Tla', 'Kursi', 'Zarqa', 'Irbid']:
                        print(f"Found {w} in {filepath}")
