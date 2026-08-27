## P(roc)E(ss)

### Overview
- Reverse challenge (102 pts). Binary là MinGW x64, in ra **flag giả**
  `PTITCTF{75c7be…}` và khi có process tên `4mCnFu.exe` đang chạy thì thực hiện
  injection 3 byte (`xor eax,eax; ret`) rồi in hint
  *"The sealed page changed somewhere else."*
- Flag thật không được in ra. Nó bị mã hoá bởi một ARX stream cipher **dead code**
  tại `0x140002379` (chỉ được trỏ từ `.data[0]`, không bao giờ được gọi).

### Các thông số (reverse từ disassembly, kiểm chứng bằng angr chạy hàm thật)
- Blob tên process @`0x14000503c` XOR `0x64` → `4mCnFu.exe`.
- Blob flag giả @`0x14000505c` XOR `0x80` → `PTITCTF{75c7be…}`.
- Salt @`0x14000502c` = `7f69fd375b06cd415d4b36aade3db1a1`.
- Key = `tolower(strip(".exe", "4mCnFu.exe"))` = **`4mcnfu`** (chữ thường).
- Nonce `arg3` = **`0`** (tìm bằng cách quét arg3 cho tới khi ra chuỗi đọc được).

### Cipher (`0x140002379`)
```
seed = FNV-1a64(FNV-1a64(FNV-1a64(offset, key), salt), arg3_le)
24-byte key = 3x splitmix64 finalizer  ->  k[0..5] (6 dword)

với mỗi block 8 byte i:
    a = (i ^ k[4]);  b = (k[5] ^ arg3)
    27 vòng ARX trên state s0=k0, s1=k1, s2=k2, s3=k3:
        a  = (ror(a,8)+b) ^ s0
        b  = rol(b,3) ^ a
        j  = r % 3
        s[j] = (ror(s[j],8)+s0) ^ r      # s[0]=s1, s[1]=s2, s[2]=s3
        s0 = rol(s0,3) ^ s[j]
    keystream = (a, b) little-endian, XOR với ciphertext
```

### Ciphertext
36 byte tại file offset `0x36b3` trong `.rdata`:
```
c6f7376d0d395504f145ce03d6a12fb159cfb57293cade18e90d9a4730885549de8ee697
```
Giải mã (key `4mcnfu`, salt ở trên, arg3=0) → plaintext leetspeak đọc được:
```
50m371m35_1nf0rm4710n_1n_42ce4d87b74
```
(= *sometimes_information_in_42ce4d87b74*)

### Flag
```
PTITCTF2026{50m371m35_1nf0rm4710n_1n_42ce4d87b74}
```

Solver: `solve/decode_final.py` (kèm `solve/verify_decoder.py` kiểm chứng bằng angr).
