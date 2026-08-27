# OmniWatch — Evidence Manifest

Target: `http://154.57.164.82:31976`
Result: `HTB{h3110_41w4y5_i_s3e_y0u4nd_1m_w4tch1ng_01df607f55a36f0a4512e62e8fa22a28}`

Files:
- `oracle_crlf_injection.txt`  — CRLF header injection confirmed in oracle (`DeviceId` reflect)
- `cache_poison.txt`           — Varnish `CacheKey` keying + `CacheKey: enable` caching
- `absent_slot.txt`            — absent vs empty CacheKey are different slots (root fix)
- `bot_creds_capture.txt`      — in-band capture of moderator creds via spoofed login page
- `secret_and_forge.txt`       — LFI jwt_secret + forged admin JWT (verified HS256)
- `sqli_signature.txt`         — stacked-SQLi signature write (string literal fix)
- `flag.txt`                   — admin page /readflag output
