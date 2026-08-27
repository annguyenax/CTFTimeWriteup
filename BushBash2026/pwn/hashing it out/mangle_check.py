import hashlib

target = '51f8aea8517e3c5b9f5f1c9744f24c3c'

base_words = [
    'bush', 'bushbash', 'lost', 'found', 'compass', 'gps', 'location', 'locate',
    'where', 'here', 'there', 'way', 'path', 'trail', 'map', 'admin', 'root',
    'user', 'login', 'password', 'secret', 'hidden', 'flag', 'ctf', 'cssa',
    'advisor', 'service', 'database', 'select', 'selection', 'comprehensive',
    'vals', 'server', 'auth', 'authenticate', 'reauth', 'welcome', 'access',
    'wander', 'wanderer', 'navigate', 'nav', 'direction', 'coordinate', 'geo',
    'travel', 'travellost', 'hike', 'hiker', 'forest', 'woods', 'trees', 'nature',
    'outdoor', 'outdoors', 'camp', 'camping', 'survive', 'survival',
]

suffixes = ['', '1', '12', '123', '1234', '!', '01', '2026', '26', '007', '99', '9', '0']
prefixes = ['', '1', '!']

candidates = set()
for w in base_words:
    variants = [w, w.lower(), w.upper(), w.capitalize()]
    for v in variants:
        for p in prefixes:
            for s in suffixes:
                cand = p + v + s
                if 0 < len(cand) <= 10:
                    candidates.add(cand)

print('total candidates:', len(candidates))
found = None
for c in candidates:
    if hashlib.md5(c.encode()).hexdigest() == target:
        found = c
        break

print('FOUND:', repr(found))
