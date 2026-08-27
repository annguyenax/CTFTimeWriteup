# extremely_original — WORKING NOTES (status: PAUSED / unsolved)

> Chưa có flag tái lập được. KHÔNG kết luận flag. File này ghi lại phân tích để tiếp tục sau.

## Đề
- Ciphertext (chép nguyên văn từ challenge.md): `oyO+UrMXccyqeo2W+WA5jZPVXNSAyYVwGt` (34 ký tự)
- "my computer generated keys to encrypt my flag before releasing it to the public"
- Flag = "LITCTF" + chuỗi ký tự.

## Hai mô hình đang cân nhắc
1. **Base64 → XOR keystream.** 34 ký tự (charset base64, không padding) decode ra **25 byte nhị phân**:
   `a3 23 be 52 b3 17 71 cc aa 7a 8d 96 f9 60 39 8d 93 d5 5c d4 80 c9 85 70 1a`.
   XOR 6 byte đầu với `LITCTF` ⇒ keystream = `ef 6a ea 11 e7 51` (đều >127 ⇒ key nhị phân, KHÔNG phải ASCII).
2. **Cipher per-char trên chuỗi 34 ký tự** (vì len(ct)=34 = len("LITCTF"+28)). XOR chuỗi thô với `LITCTF`
   ⇒ keystream = `23 30 1b 68 01 34` (đều <127). Không có chu kỳ ngắn.

## Đã thử và LOẠI TRỪ (đều trượt, có evidence)
- single-byte XOR; repeating-key XOR chu kỳ ngắn (không khớp 6 byte).
- Vigenère ASCII (xor/add/sub) — **bất khả thi** cho mô hình base64 vì key-byte yêu cầu >127.
- Python `random`: `randbytes` seed 0–20M; `getrandbits(8)`/`randint(0,255)` seed 0–30M; big-endian `getrandbits(200)` 0–3M; add/sub 0–3M. (cả mô hình base64 và raw-string tới 2M).
- repeating `randbytes(k)` key, k=1..25 (timeout, chưa phủ hết — CẦN CHẠY LẠI).
- `numpy.random.RandomState.bytes` seed 0–300k.
- LCG byte `x=a*x+c mod256`: brute toàn bộ (a,c) — không (a,c) nào tái tạo được 6 byte keystream.
- RC4 với khóa ứng viên; XOR với `sha256(key)` lặp.
- `random.shuffle` S-box seed 0–400k; **shuffled/custom Base64 alphabet** seed 0–2M (chỉ suy được 8/24 ánh xạ, không phải phép quay nên không ngoại suy).
- Affine per-byte (số nguyên); autokey/CFB/OFB feedback.
- Unpadded RSA (căn bậc e nguyên của big-int, e=2..65537) — không exact.
- Seed = timestamp cửa sổ 2026-06→08 (randbytes/getrandbits) — trượt.
- keystream = md5/sha1/sha256 của seed nhỏ (0–500k, nhiều cách encode) — trượt.

## Giả thuyết còn lại (NEXT STEPS, ưu tiên)
1. **Hoàn tất repeating `randbytes(k)`** (k=6..24) seed 0–5M mà không timeout (tách từng k, tối ưu).
2. **PRNG khác Python**: JavaScript `Math.random` (xorshift128+), PHP `mt_rand`/`rand`, Java `Random` (LCG 48-bit) — sinh keystream theo đúng thuật toán rồi brute seed.
3. Seed = **timestamp** nhưng khác cửa sổ (thử toàn 2025, hoặc mốc epoch nhỏ hơn), cho cả 2 mô hình.
4. Tìm **known plaintext dài hơn**: nếu flag có định dạng `LITCTF{...}` và đuôi `}`, thêm crib để phát hiện chu kỳ/khôi phục state.
5. Xem lại giả định base64: thử base85/ascii85, hoặc chuỗi là **big-int** cho một scheme modular có tham số ẩn.

## Nguyên tắc
Không viết flag vào bất kỳ đâu cho tới khi tái lập được bằng giải mã xác định. Bài đang PAUSED.
