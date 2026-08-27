# It's Oops PM

**Thể loại:** hw (hardware) · **Độ khó:** very easy · **Tác giả:** makelaris
**Nguồn:** HackTheBox Try Out

## 1. Đề bài

Các cảm biến môi trường liên lạc với một vệ tinh qua một crypto-processor (TPM) mã hoá
đường truyền. Khi phục dựng logic chip bằng VHDL, đội ngũ phát hiện một **backdoor**:
nó chỉ kích hoạt khi đầu vào đúng một giá trị đặc biệt. Nhiệm vụ: "kết nối vệ tinh và
kích hoạt nó" — tức tìm input kích hoạt backdoor để lấy flag.

## 2. Kiến thức nền

- VHDL: `STD_LOGIC_VECTOR(15 downto 0)` = bit 15..0 (MSB trước).
- Trong một `process`, phép gán tín hiệu **sau cùng thắng** (sequential override).
- MUX: chọn một trong hai ngõ vào theo tín hiệu điều khiển `B`.

## 3. Phân tích

- `key.vhdl`: hằng `K = "0110001111100001"` = **0x63E1**.
- `backdoor.vhdl`: hằng `pattern = "1111111111101001"` = **0xFFE9**;
  so sánh `D = pattern` (không mask) → `B = '1'`.
- `encryption.vhdl`: `E(i) = D(i) XOR K(i)` với `i = 1..15`, rồi ghi đè
  `E(0) = NOT K(0)`, `E(6) = NOT K(6)`, `E(13) = NOT K(13)` — cipher bị vỡ:
  ba bit này của bản mã **không phụ thuộc dữ liệu**, chỉ lộ `NOT K`.
- `tpm.vhdl`: `Output = Key` khi `B='1'` (backdoor), ngược lại `Output = Encrypted`.

Mô phỏng Python (tái hiện đúng thứ tự gán của VHDL):
`encrypt(0xFFFF) = 0x9C1E`, `encrypt(0x0000) = 0x43A0`, `tpm(0xFFE9) = 0x63E1` — khớp
tính tay, xác nhận backdoor leak **key**.

## 4. Vì sao hướng này

- Không cần brute 2^16: pattern nằm sẵn trong `backdoor.vhdl`.
- Không cần phá XOR thủ công: backdoor làm MUX xuất thẳng **KEY** thay vì ciphertext.
- Input kích hoạt = `1111111111101001`; sau khi có key, có thể giải mã truyền tin
  (trừ bit 0/6/13 bị mất).

## 5. Các bước

1. Giải nén `files/hardware_its_oops_pm.zip` → 4 file VHDL + `schematic.png`.
2. Đọc VHDL → trigger `0xFFE9`, key `0x63E1`, công thức mã hoá vỡ.
3. Chạy `python solve/solve.py` để mô phỏng TPM và xác minh giá trị.
4. Target: `154.57.164.82:31090` — banner `The input must be a binary signal of 16 bits.`
5. Gửi `1111111111101001` → `Output: 0110001111100001` (đúng KEY) + flag.
6. Replay TCP độc lập → cùng flag.

```text
python solve/solve.py --target 154.57.164.82:31090
```

## 6. Flag
```
HTB{4_7yp1c41_53cu23_TPM_ch1p}
```
