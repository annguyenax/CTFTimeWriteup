# Warmy â€” Writeup (Kali Team CTF 26 / Pwn)

## 1. Äá» bÃ i yÃªu cáº§u gÃ¬?

- Binary Linux 64-bit kÃ¨m `libc.so.6`, loader vÃ  `flag.txt` máº«u.
- Prompt: *"Its Simple"* (author JO0031).
- Loáº¡i: `dynamic_docker` trÃªn platform (remote sau khi Start instance).
- Má»¥c tiÃªu: Ä‘á»c flag dáº¡ng `KaliTeam{...}` (file `flag.txt` cáº¡nh binary).

Trong gÃ³i bÃ i, `flag.txt` local lÃ  **`KaliTeam{fake_flag}`** â€” dÃ¹ng Ä‘á»ƒ xÃ¡c minh exploit offline. Flag tháº­t chá»‰ cÃ³ trÃªn instance remote.

## 2. Kiáº¿n thá»©c ná»n cáº§n cÃ³

| KhÃ¡i niá»‡m | VÃ¬ sao cáº§n |
|---|---|
| Stack frame (`buf`, saved RBP, saved RIP) | Biáº¿t offset ghi Ä‘Ã¨ return address |
| Buffer overflow vá»›i `gets()` | HÃ m khÃ´ng giá»›i háº¡n Ä‘á»™ dÃ i â†’ classic BOF |
| Protections: Canary / NX / PIE / RELRO | Chá»n hÆ°á»›ng khai thÃ¡c |
| ret2win | CÃ³ sáºµn hÃ m `win()` in flag â†’ khÃ´ng cáº§n ROP phá»©c táº¡p |
| Little-endian `p64(addr)` | ÄÃ³ng gÃ³i Ä‘á»‹a chá»‰ trÃªn x86-64 |

## 3. PhÃ¢n tÃ­ch (triage)

### Protections

```
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        No PIE (0x400000)
```

- **KhÃ´ng canary** â†’ overflow stack thoáº£i mÃ¡i.
- **NX báº­t** â†’ khÃ´ng nháº£y vÃ o shellcode trÃªn stack.
- **KhÃ´ng PIE** â†’ Ä‘á»‹a chá»‰ `win` cá»‘ Ä‘á»‹nh (`0x401236`).

### Luá»“ng chÆ°Æ¡ng trÃ¬nh

1. `main`: `setvbuf` stdin/stdout â†’ gá»i `vuln()`.
2. `vuln`:
   - `puts("Hola! ")` (banner),
   - `gets(buf)` vá»›i `buf` táº¡i **`[rbp-0x40]`**.
3. `win`:
   - `fopen("flag.txt", ...)`,
   - in `"The Flag: "`,
   - Ä‘á»c tá»«ng kÃ½ tá»± báº±ng `fgetc`/`putchar`,
   - Ä‘Ã³ng file.

PLT cÃ³ `gets` â†’ tÃ­n hiá»‡u overflow ráº¥t rÃµ.

## 4. VÃ¬ sao chá»n ká»¹ thuáº­t ret2win?

| Giáº£ thuyáº¿t | Test ráº» | Káº¿t quáº£ |
|---|---|---|
| A. ret2win qua `gets` | Xem symbol `win` + offset stack | **ÄÃºng** â€” cÃ³ `win`, no canary, no PIE |
| B. Format string | KhÃ´ng tháº¥y `printf(user)` | Loáº¡i |
| C. ROP/libc leak | Cáº§n náº¿u khÃ´ng cÃ³ `win` / cÃ³ PIE+canary | KhÃ´ng cáº§n |

ThÃ´ng tin gain cao nháº¥t: ghi Ä‘Ã¨ RIP = `win`.

## 5. CÃ¡c bÆ°á»›c khai thÃ¡c

1. XÃ¡c Ä‘á»‹nh offset:
   - `sub rsp, 0x40` + buffer táº¡i `rbp-0x40`
   - saved RBP: 8 byte
   - **OFFSET = 0x48 (72)** tá»›i saved RIP
2. Payload:

```text
[ 72 bytes padding ][ 8 bytes address of win ]
```

3. Gá»­i sau banner `Hola! `.
4. `win` in ná»™i dung `flag.txt`.

Sau `win` return, process thÆ°á»ng **segfault** (RIP trá» rÃ¡c) â€” bÃ¬nh thÆ°á»ng náº¿u Ä‘Ã£ in flag.

## 6. Solver / lá»‡nh tá»‘i thiá»ƒu

File: `solve/solve.py`

```bash
# Local (trong files/player hoáº·c qua solve.py tá»± tÃ¬m binary)
python3 solve/solve.py

# Remote
python3 solve/solve.py remote HOST PORT
```

Payload cá»‘t lÃµi:

```python
OFFSET = 0x48
payload = b"A" * OFFSET + p64(elf.symbols["win"])
```

## 7. XÃ¡c minh flag

**Local (Ä‘Ã£ tÃ¡i láº­p):**

```text
Hola! 

The Flag: KaliTeam{fake_flag}
```

Evidence: `solve/evidence/local_run.txt`

**Remote:** Start container trÃªn `kali-team.online`, cháº¡y `solve.py remote <host> <port>`, flag tháº­t khÃ¡c `fake_flag`.

## 8. BÃ i há»c vÃ  lá»—i thÆ°á»ng gáº·p

| Lá»—i | CÃ¡ch trÃ¡nh |
|---|---|
| Offset 0x40 thay vÃ¬ 0x48 | Nhá»› cá»™ng 8 byte saved RBP |
| Gá»i `win+4` bá» `endbr64` | KhÃ´ng cáº§n; `endbr64` an toÃ n khi nháº£y vÃ o Ä‘áº§u hÃ m |
| QuÃªn cwd / khÃ´ng cÃ³ `flag.txt` | Cháº¡y process vá»›i `cwd` lÃ  thÆ° má»¥c chá»©a `flag.txt` |
| Stack alignment 16-byte cho `system` | ret2win fopen/printf thÆ°á»ng OK; ROP `system` má»›i hay cáº§n `ret` gadget |
| Coi `fake_flag` lÃ  flag thi | Chá»‰ lÃ  file máº«u trong zip |

## 9. TÃ³m táº¯t má»™t dÃ²ng

**`gets` overflow 72 byte â†’ ghi Ä‘Ã¨ RIP báº±ng `win@0x401236` â†’ in `flag.txt`.**

## Remote flag (verified)

```text
KaliTeam{e8b9c40c-bd93-454f-96a1-fb8b9470ac0a}
``` 

Host: `chall.kali-team.online:10017`
