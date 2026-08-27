#!/usr/bin/env python3
# Run INSIDE the running backend container (Django + deps installed), from /app:
#   docker compose ps                       # find the backend service name (e.g. 'web')
#   docker compose cp findmod.py <svc>:/app/findmod.py
#   docker compose exec <svc> python /app/findmod.py
#
# It reproduces daphne startup (imports config.asgi.application), then drives every endpoint via the
# Django test client, and prints modules imported FRESH afterwards + their file path. We want a module
# whose origin is a top-level  /usr/local/lib/python3.11/<name>.py   OR one level deep under a package
# dir reachable by zip-slip (json/ email/ http/ xml/ — because 'lib/python3.11/<pkg>' <= 20 chars).
import os, io, zipfile, sys, json as _json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# ---- reproduce daphne startup import state ----
from config.asgi import application  # noqa  (does django.setup + loads URLconf, like daphne)
import django
BASE = set(sys.modules)

from django.test import Client
c = Client()

def tok():
    c.post('/api/auth/register/', data=_json.dumps({'username': 'zz1', 'password': 'Passw0rd!1'}), content_type='application/json')
    r = c.post('/api/auth/login/', data=_json.dumps({'username': 'zz1', 'password': 'Passw0rd!1'}), content_type='application/json')
    return r.json().get('access', '')

t = tok()
H = {'HTTP_AUTHORIZATION': 'Bearer ' + t}
for path in ('/api/schema/', '/api/schema/?format=json', '/api/schema/?format=yaml', '/api/docs/', '/api/mods/', '/api/platforms/', '/api/auth/me/'):
    try: c.get(path, **H)
    except Exception as e: print('  req err', path, e)

# create platform+mod+build then upload a zip (exercise the upload code path)
try:
    pid = c.post('/api/platforms/', data=_json.dumps({'code': 'pc1', 'name': 'p'}), content_type='application/json', **H).json()['id']
    mid = c.post('/api/mods/', data=_json.dumps({'title': 'm', 'mod_version': 'v1'}), content_type='application/json', **H).json()['id']
    bid = c.post(f'/api/mods/{mid}/builds/', data=_json.dumps({'platform': pid}), content_type='application/json', **H).json()['id']
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('a.txt', b'hello')
    b.seek(0)
    from django.core.files.uploadedfile import SimpleUploadedFile
    c.post(f'/api/mods/{mid}/builds/{bid}/upload/', {'zip_file': SimpleUploadedFile('p.zip', b.read(), 'application/zip')}, **H)
except Exception as e:
    print('  upload path err', e)

NEW = sorted(set(sys.modules) - BASE)
print("\n=== modules imported FRESH after startup (name -> origin) ===")
for name in NEW:
    m = sys.modules.get(name)
    origin = getattr(getattr(m, '__spec__', None), 'origin', None) or getattr(m, '__file__', None)
    print(f"{name}\t{origin}")

print("\n=== REACHABLE targets (overwritable via zip-slip) ===")
for name in NEW:
    m = sys.modules.get(name)
    origin = getattr(getattr(m, '__spec__', None), 'origin', None) or getattr(m, '__file__', None) or ''
    if not origin.endswith('.py') or 'site-packages' in origin:
        continue
    # top-level: /usr/local/lib/python3.11/NAME.py   OR one-level pkg reachable (json/email/http/xml)
    rel = origin.split('/python3.11/')[-1] if '/python3.11/' in origin else origin
    parts = rel.split('/')
    if len(parts) == 1:
        print(f"[TOP]  {name} -> platform_code='lib/python3.11' entry='{parts[0]}'")
    elif len(parts) == 2 and parts[0] in ('json', 'email', 'http', 'xml'):
        print(f"[PKG]  {name} -> platform_code='lib/python3.11/{parts[0]}' entry='{parts[1]}'  (pc len={len('lib/python3.11/'+parts[0])})")
