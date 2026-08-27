# carnival_game — Writeup (LIT2026 / Crypto)

## 1. Đề bài yêu cầu gì
> Booth hội chợ bắt đoán đúng **5 số liên tiếp** (mỗi số 0–99) để thắng. Để chứng minh
> không gian lận, nó công bố `SHA256(server_seed)`. `nc 136.115.87.65 31783`

File: `carnival-game.py`. Nhiệm vụ: đoán trúng 5 vòng để server in flag.

## 2. Kiến thức nền
- **Commitment scheme.** Server "cam kết" seed bằng cách công bố `SHA256(seed)` trước,
  để sau này không đổi seed. Nhưng commitment cũng cho ta **cách kiểm tra** một seed đoán được.
- **PRNG seed theo thời gian.** `random.Random(int(time.time()))` là Mersenne Twister
  seed bằng **thời gian Unix theo giây**. Không gian seed rất nhỏ (mỗi giây 1 giá trị).
- **Hàm roll tất định:** `roll(seed, round) = int(SHA256(f"{seed}-{round}"),16) % 100`.
  Biết `seed` là biết mọi roll.

## 3. Phân tích code
```python
seed = random.Random(int(time.time())).randbytes(16).hex()   # phụ thuộc DUY NHẤT vào giây hiện tại
print(f"commitment:{sha(seed)}")                              # lộ SHA256(seed)
...
r = roll(seed, round)                                         # roll tất định theo seed
if guess == r: streak += 1 ...                                # đủ 5 streak -> in flag
```
**Lỗ hổng:** `seed` không hề ngẫu nhiên mật mã — nó bị quyết định hoàn toàn bởi
`int(time.time())` lúc kết nối. Và commitment `SHA256(seed)` cho ta oracle để xác nhận.

## 4. Lý do chọn kỹ thuật
Khi kết nối, ta biết thời gian hiện tại xấp xỉ (đồng hồ ta lệch server vài giây).
Chỉ cần **brute vài chục giá trị giây**, tính lại `random.Random(t).randbytes(16).hex()`,
băm SHA256 và so với commitment. Trùng ⇒ tìm đúng `seed`. Không cần đoán mò.

## 5. Các bước khai thác
1. Kết nối, đọc `commitment:<hex>`.
2. `for t in range(now+5, now-120, -1)`: nếu `sha256(random.Random(t).randbytes(16).hex()) == commitment` → `seed = ...`.
3. Với mỗi vòng `round`, gửi `guess = roll(seed, round)`.
4. Sau 5 lần đúng, server in flag.

Solver mạng: `../solve/solve.py`. Kiểm thử offline: `../solve/local_test.py`.

## 6. Cách xác minh
Vì đây là bài **remote** và buổi học **offline (không kết nối, không submit)**, tôi xác minh
kỹ thuật bằng **kiểm thử end-to-end cục bộ**: chạy chính `carnival-game.py` làm tiến trình con
với `flag.txt` giả, để solver chơi. Kết quả (`../solve/evidence/local_run.txt`):
```
Congratulations! Here's your flag b'LITCTF{fake_flag_for_local_test}'
WIN: True
```
Solver khôi phục đúng seed từ commitment và thắng 5/5 → chạy với server thật sẽ in flag thật.

## 7. Flag
**Chưa lấy (bài remote, học offline).** Flag thật nằm trong `flag.txt` phía server; chạy
`python solve.py 136.115.87.65 31783` khi có kết nối sẽ in ra. Không bịa flag.

## 8. Bài học & lỗi thường gặp
- **`random` KHÔNG phải mật mã.** Seed theo `time.time()` là brute-force được ngay.
  Dùng `secrets`/`os.urandom` cho seed mật mã.
- **Commitment giúp kẻ tấn công** khi seed yếu: nó biến "đoán seed" thành có thể kiểm chứng.
- Khi khai thác PRNG theo thời gian, **brute một cửa sổ giây** quanh thời điểm kết nối
  (đồng hồ client/server lệch nhau) thay vì đúng 1 giá trị.
- Verify bằng **oracle sẵn có** (ở đây là commitment) trước khi tương tác nhiều với server.
