import urllib.request, json
body = b'{"symbols":{"puts":"cc0"}}'
req = urllib.request.Request('https://libc.rip/api/find', data=body,
                             headers={'Content-Type':'application/json'})
try:
    r = json.loads(urllib.request.urlopen(req, timeout=40).read())
    print('total', len(r))
    for x in r:
        if 'amd64' in x['id'] or '_64' in x['id'] or 'x86_64' in x['id'] or x['id'].endswith('_amd64'):
            print(x['id'], 'puts', x['symbols'].get('puts'), 'system', x['symbols'].get('system'))
except Exception as e:
    print('ERR', e)
