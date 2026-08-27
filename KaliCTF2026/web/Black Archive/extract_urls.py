import re

with open("index.js", "r", encoding="utf-8") as f:
    content = f.read()

urls = re.findall(r'["\'](/api/[^"\']+)["\']', content)
print("Found API routes:", set(urls))

paths = re.findall(r'path:\s*["\']([^"\']+)["\']', content)
print("Found client routes:", set(paths))
