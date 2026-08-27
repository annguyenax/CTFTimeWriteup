import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django.conf.global_settings')
import django
django.setup()
from django.test import RequestFactory

rf = RequestFactory()
pre = set(sys.modules)
body = b'--boundary\r\nContent-Disposition: form-data; name="test"\r\n\r\nhello\r\n--boundary--\r\n'
req = rf.post('/api/mods/', data=body, content_type='multipart/form-data; boundary=boundary; charset=iso8859_2')
print('POST data:', req.POST)
post = set(sys.modules) - pre
print('Fresh modules:', [m for m in post if 'iso8859' in m or 'encodings' in m])
