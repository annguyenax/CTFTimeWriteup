# SSSH — phân tích & lời giải (cho grok implement)

Nguồn: `files/server.py`. Bài instance-based, TCP (và cùng port phục vụ HTTP download).

## Lỗ hổng cốt lõi (2 cái, kết hợp)
1. **DH shared bị bypass**: `KeyExchange.accept` KHÔNG chặn `client_pub` tầm thường. Gửi `client_pub = "1"` →
   `shared = 1^private mod P = 1` → `shared_bytes = b"\x01"`. Ta biết TRỌN vẹn input của session_id.
   `session_id = sha256(b"SSSH session|" + b"\x01" + client_nonce + server_nonce).hexdigest()`
   (client_nonce do ta chọn; server_nonce trả về trong kex_reply).
2. **Chữ ký RSA chỉ verify 16 bit thấp** (`SignatureVerifier.verify`):
   `recovered = pow(sig, e, n); return (recovered & 0xFFFF) == sha256(message)[-2:]`
   → forge được mà không cần private key. **`n, e=3` LÀ session key mà server đưa cho client** qua challenge.txt
   (`verifier = SignatureVerifier(n, e)` với n,e từ `generate_session_public_key()` — e cố định = 3).

## Message được ký
`message = f"SSSH-AUTH|{session_id}|user=ctf".encode()`  (user PHẢI = "ctf").
Cần `sig` sao cho `pow(sig,3,n) & 0xFFFF == int.from_bytes(sha256(message)[-2:],"big")`. Brute ~65536 lần.

## Protocol đầy đủ
1. TCP connect (nc). Server gửi intro chứa URL:
   `http://<same-host>:<same-port>/download/<token>/challenge.txt`  → **lấy token từ intro**.
2. Mở HTTP GET tới cùng host:port: `GET /download/<token>/challenge.txt` → nội dung có các dòng
   `NN: <52-char b64 chunk>`. Ghép các chunk theo thứ tự → base64-decode → **PEM** của RSA pubkey.
   Parse PEM (SubjectPublicKeyInfo DER) → lấy `n` (e=3).
3. Quay lại TCP, gửi `start\n`.
4. Menu: gửi `2\n`, đợi `kex_init json>`, gửi 1 dòng JSON:
   `{"type":"kex_init","client_pub":"1","client_nonce":"<base64(16 rand bytes)>"}`
   Đọc kex_reply JSON → lấy `server_nonce` (b64). Tính session_id (công thức trên).
5. Gửi `3\n`, đợi `auth json>`, brute sig, gửi:
   `{"action":"auth","user":"ctf","signature":"<hex(sig)>"}` → chờ `auth accepted`.
6. Gửi `4\n` → shell. Chạy `ls`, `ls /`, `cat flag.txt`, `cat /flag.txt`, `cat /app/flag*`.
   (Shell có: help/pwd/ls/cd/cat/id/whoami/sudo su. `sudo su` cần root password random → tránh; flag đọc bằng `cat`.)

## Skeleton (pwntools)
```python
from pwn import *; import json, hashlib, base64, re, os
H,P='144.79.188.39', <PORT>          # instance hiện tại
io = remote(H,P)
intro = io.recvuntil(b"type 'start'")
tok = re.search(rb"/download/([A-Za-z0-9]+)/challenge.txt", intro).group(1).decode()
# fetch challenge.txt over HTTP (new connection, same host:port)
h = remote(H,P); h.send(f"GET /download/{tok}/challenge.txt HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n".encode())
raw = h.recvall(timeout=5); h.close()
body = raw.split(b"\r\n\r\n",1)[1].decode()
chunks = re.findall(r"^\d+:\s*([A-Za-z0-9+/=]+)$", body, re.M)
der = base64.b64decode("".join(chunks))
# parse SPKI DER -> n (reuse server's DerReader logic): top seq -> skip algid seq -> bitstring -> seq(n,e)
def spki_n(der):
    from server import DerReader   # or inline the class
    t=DerReader(der).read_sequence(); t.read_sequence(); bs=t.read_bit_string()
    r=DerReader(bs).read_sequence(); return r.read_integer(), r.read_integer()
n,e = spki_n(der)                    # e==3
io.send(b"start\n")
io.sendlineafter(b"choice>", b"2"); io.recvuntil(b"kex_init json>")
cn = os.urandom(16)
io.sendline(json.dumps({"type":"kex_init","client_pub":"1","client_nonce":base64.b64encode(cn).decode()}).encode())
rep = json.loads(io.recvuntil(b"}").split(b"kex accepted\n")[-1])
sn = base64.b64decode(rep["server_nonce"])
sid = hashlib.sha256(b"SSSH session|"+b"\x01"+cn+sn).hexdigest()
msg = f"SSSH-AUTH|{sid}|user=ctf".encode()
tgt = int.from_bytes(hashlib.sha256(msg).digest()[-2:],"big")
sig=1
while pow(sig,e,n)&0xFFFF != tgt: sig=int.from_bytes(os.urandom((n.bit_length()+7)//8),"big")%n or 1
io.sendlineafter(b"choice>", b"3"); io.recvuntil(b"auth json>")
io.sendline(json.dumps({"action":"auth","user":"ctf","signature":format(sig,"x")}).encode())
io.recvuntil(b"auth accepted")
io.sendlineafter(b"choice>", b"4")
io.sendline(b"ls /"); io.sendline(b"cat /flag.txt"); io.sendline(b"cat flag.txt")
io.interactive()
```
Lưu ý: đọc/parse framing menu cho khớp (server in `\nchoice>\n`). Chỉnh `recvuntil` nếu cần.
