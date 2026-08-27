# TunnelMadness — HTB TryOut (rev, medium)

## Tóm tắt
`tunnel` là ELF64 x86-64, PIE, không strip. Chương trình đưa người chơi đi trong
mê cung 3D `20×20×20` bằng các phím hướng `L/R/F/B/U/D` (`Q` để thoát). Khi tới ô
đích, nó gọi `get_flag()` → `fopen("/flag.txt")` và in nội dung. Toàn bộ mê cung
được **nhúng trong `.rodata`**, nên đây là bài trích dữ liệu + tìm đường offline,
không phải khai thác memory corruption.

## Phân tích
- `get_cell()` (0x11b5): `addr = maze + 16*(400*x + 20*y + z)`. Mỗi cell 16 byte,
  trường loại ở offset `+0x0c`: `0`=start, `1`=phòng đi được, `2`=tường, `3`=đích.
- `maze` @ VA `0x20e0`, dài `0x1f400` = 8000 cell.
- `prompt_and_update_pos()` (0x11e3) đọc 1 ký tự (`scanf(" %c")`), `toupper`, rồi
  dispatch qua jump table. Mapping (giải mã từ bảng nhảy + thân case):
  `L: x-1  R: x+1  B: y-1  F: y+1  D: z-1  U: z+1`; mỗi hướng kiểm tra biên `0..19`
  và từ chối nếu ô đích có loại `2`.
- `main()` (0x1538) lặp tới khi ô hiện tại có loại `3` rồi gọi `get_flag()`.

## Lời giải
Trích blob `maze` từ `.rodata`, dựng graph 3D (bỏ ô loại 2, cạnh nối 6 hàng xóm),
BFS từ `(0,0,0)` tới ô loại 3 tại `(19,19,19)`. Đường ngắn nhất là **duy nhất**,
dài **59 bước**; đổi các delta tọa độ sang ký tự hướng, kiểm tra lại bằng mô phỏng
từng bước (mọi bước hợp lệ, kết thúc đúng ô đích).

Chuỗi input (khóa mở mê cung):

```
UUURFURURRFRRFFUUFURRUFUFFRFUFUUUUFFRRUUUFURFDFFUFFRRRRRFRR
```

Nạp chuỗi này vào service từ xa → chương trình in `/flag.txt` (flag thật nằm phía
server). Bản offline chỉ có fallback `HTB{fake_flag_for_testing}` khi thiếu file.

Chạy: `python solve/solve.py files/_work/rev_tunnelmadness/tunnel`

## Ghi chú flag
Flag thật lấy từ `/flag.txt` trên instance khi đi hết mê cung; không có instance
kèm theo nên đây là **chuỗi lời giải đã kiểm chứng offline**, không phải flag thật.
Không bịa flag.

## Khắc phục
Đừng nhúng toàn bộ topology + logic xác minh phía client. Nếu mê cung phải bí mật,
xác minh tiến trình ở phía server có integrity/session. Strip symbol không phải
ranh giới bảo mật.

## Kết quả live (verified 2026-08-20)
Nạp 59 ký tự đường đi vào instance → chương trình in
`You break into the vault and read the secrets within...` rồi flag từ `/flag.txt`:

```
HTB{tunn3l1ng_ab0ut_in_3d_54c8d4fe3a8eec9a4e6259a56f78042c}
```
Xác nhận BFS offline đúng; hash cuối là per-instance (từ `/flag.txt` phía server).
