# Welcome to CTF — HTB TryOut (general, sanity check)

## Tóm tắt
Bài onboarding. Web app Flask/Werkzeug (`Server: Werkzeug/3.0.2 Python/3.12.3`)
tại instance được cấp. Flag in thẳng trong nội dung trang chủ.

## Lời giải
Truy cập `http://<IP>:<PORT>/` và đọc đoạn onboarding:

```
Congratulations, you've got your first flag. Please copy and paste your flag
onto the platform: HTB{onboard1ng_fl4g}.
```

Reproduce:
```
curl -s http://154.57.164.82:30352/ | grep -oE 'HTB\{[^}]*\}'
```

## Flag
`HTB{onboard1ng_fl4g}`  (verified live)
