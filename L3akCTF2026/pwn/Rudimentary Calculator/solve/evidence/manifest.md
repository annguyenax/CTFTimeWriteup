# Evidence manifest — Rudimentary Calculator

| File | Claim supported | Source/tool | Reproduction | Why kept |
|---|---|---|---|---|
| ../exploit.py | Chuỗi khai thác: leak canary+PIE qua `len` corruption, ghi `win`+canary qua scanf-null, return vào win | Python ssl socket | `python solve/exploit.py` | Solver tái lập |
| run_transcript.txt | Bằng chứng exploit lấy flag trên instance chính thức | stdout | như trên | Xác minh flag |
| ../../files/pwn_rudimentary-calculator/chall.c | Source: bignum overflow + canary + win() | archive | đọc | Chứng minh lỗ hổng |

## Kết quả xác minh

- `python solve/exploit.py` → `L3AK{s3Arch_f0r_Sm0otH}` (attempt 0).
- **Verify mạnh:** flag do `win()` đọc `flag.txt` in ra trên **server challenge chính thức**, qua chuỗi exploit tái lập (leak → ghi → return).
- Leak nhất quán: canary LSB = 0x00; `ret & 0xfff == 0xa9b` khớp offset return-into-main `0x1a9b`; `pie & 0xfff == 0`.

Artifact gốc: `files/pwn_rudimentary-calculator.tar.gz`
SHA-256: `00c9719873a0631136d6c22b357688d0947c600eb974290fad830c47efaa4ba8`
