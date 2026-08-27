import re

data = open('entry_app.js', encoding='utf-8').read()
print('file length:', len(data))

pairs = re.findall(r'"(/[^"]*)":\[(\d+)', data)
print('total route entries found:', len(pairs))
with open('routes_dump.txt', 'w', encoding='utf-8') as f:
    for path, idx in pairs:
        f.write(f'{idx}\t{path}\n')
