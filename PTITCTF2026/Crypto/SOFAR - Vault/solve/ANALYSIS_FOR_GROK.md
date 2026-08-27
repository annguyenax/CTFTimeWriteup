# SOFAR - Vault — phân tích & lời giải (cho grok)

Theme: SOFA Score Fantasy World Cup. File: `extracted/SOFAR - Vault/` gồm ảnh + `script.py` + `format.txt` + `Maybe sth in here.bin`.

## Luồng 3 bước
### B1. OCR 8 fragments từ ảnh
- CÓ ĐÚNG 8 ảnh vòng đấu = 8 fragment. Thứ tự giải World Cup 2026 (sớm→muộn):
  **`R1, R2, R3` (3 lượt vòng bảng) → `R32, R16, QF, SF, F` (knockout)**. Đây là `t[0..7]`.
  (8 ảnh chữ lẻ `g,i,n,o,r,s,w,}` = có thể là nhãn/gợi ý riêng — xác nhận khi OCR, đừng nhầm với 8 fragment vòng đấu.)
- Mỗi ảnh có 1 text-band chứa 1 fragment (chuỗi ký tự). Prior đã crop/deskew ở `solve/deskew/`, `solve/crops/`.
- **Việc cần**: OCR sạch từng band → 8 strings `frag1..frag8` (đúng thứ tự vòng đấu). Dùng tesseract trên ảnh deskew, hoặc đọc tay (chỉ 8 chuỗi).

### B2. script.py → passphrase
`script.py`:
```python
t = "frag1 frag2 ... frag8".split()          # 8 fragments đã OCR, đúng thứ tự
g = "0123456789bcdefghjkmnpqrstuvwxyz"        # base32 (Crockford, bỏ i,l,o,u)
print("".join(g[eval('^'.join(str(ord(c)&31) for c in col))] for col in zip(*t)))
```
→ XOR theo cột `(ord(c)&31)` của 8 fragment cùng độ dài → index vào `g` → **passphrase**.
(Điều kiện: 8 fragment PHẢI cùng độ dài. Nếu lệch → OCR sai, sửa lại.)

### B3. Giải `Maybe sth in here.bin` bằng zip-twist-v1
Theo `format.txt` (chiều encrypt):
```
seed = SHA256(b"zip-twist-v1|" + passphrase_ascii)
block_i = SHA256(seed + u32be(i))            # keystream 32 byte/block, i=0,1,2...
tmp = plaintext_byte XOR block_i[j]          # j = vị trí byte trong block (0..31)
cipher_byte = ROL8(tmp, rotation)
output = reverse(all cipher bytes)
```
**Decrypt (đảo ngược):**
```python
import hashlib, struct
def ror8(b,r): r&=7; return ((b>>r)|(b<<(8-r)))&0xff
def decrypt(blob, passphrase, rotation):
    ct = blob[::-1]                                   # undo reverse
    seed = hashlib.sha256(b"zip-twist-v1|"+passphrase.encode()).digest()
    out=bytearray()
    for i in range((len(ct)+31)//32):
        block = hashlib.sha256(seed+struct.pack(">I",i)).digest()
        for j in range(32):
            k=i*32+j
            if k>=len(ct): break
            tmp = ror8(ct[k], rotation)               # undo ROL8
            out.append(tmp ^ block[j])                # undo XOR
    return bytes(out)
# rotation chưa biết -> brute 0..7, chọn output chứa "PTITCTF{" hoặc là PNG/ZIP hợp lệ
blob=open("Maybe sth in here.bin","rb").read()
for rot in range(8):
    pt=decrypt(blob,PASSPHRASE,rot)
    if b"PTITCTF" in pt or pt[:4] in (b"\x89PNG",b"PK\x03\x04"): print(rot, pt[:80])
```
Flag `PTITCTF{...}` (hoặc file lồng cần mở tiếp).

## Ghi chú
- Nếu `rotation` được suy từ passphrase/seed, kiểm lại format.txt bản đầy đủ. Mặc định brute 0..7 là đủ.
- Ảnh chữ lẻ (`o,r,i,g,n,s,w,},F,...`) có thể là gợi ý ("origins"?) hoặc chính là fragment — xác nhận khi OCR.
