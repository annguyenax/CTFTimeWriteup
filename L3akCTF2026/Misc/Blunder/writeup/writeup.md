# Blunder

## Đề bài yêu cầu gì?

Đề cho 24 ván cờ trong `games.pgn`, nói rằng có một “bài học” ẩn trong các ván và yêu cầu bọc đáp án bằng `L3AK{}`.

Flag thu được là:

```text
L3AK{HARD_TO_KEEP_UP_WITH_THE_QUEEN}
```

## Kiến thức nền

PGN (Portable Game Notation) ghi một ván cờ bằng các header và danh sách nước đi ở dạng SAN. Ví dụ `Qf3` nghĩa là hậu đi tới ô `f3`, còn `Qxf7+` nghĩa là hậu bắt quân tại `f7` và chiếu vua.

Mỗi ô cờ có một tọa độ gồm cột `a`–`h` và hàng `1`–`8`. Vì vậy, nếu lấy liên tiếp các ô đích của cùng một quân rồi nối chúng lại, ta nhận được một polyline trên lưới 8×8.

Tài liệu tham khảo:

- [python-chess: PGN parsing](https://python-chess.readthedocs.io/en/stable/pgn.html)
- [Stockfish: download and usage](https://official-stockfish.github.io/docs/stockfish-wiki/Download-and-usage.html)

## Phân tích ban đầu

File có SHA-256:

```text
045e6724243e8413e41989af7d550e6992aa3bc2dc4b5f5be1c623510e9de6bf
```

Có đúng 24 ván. Các ván trông rất không tự nhiên: hậu trắng liên tục đi qua nhiều ô gần nhau, đôi khi quay lại cùng một đoạn. Ví dụ ván 1 có chuỗi ô đích:

```text
f3 f4 f5 f6 e5 d5 c5 b4 b5 b6 b7 b6 b5 b4 b3 ... f6 f7
```

Ban đầu tên bài “Blunder” gợi ý dùng engine để tìm nước sai. Thử đánh giá centipawn loss bằng Stockfish tạo ra nhiều dao động mate score và không cho một blunder duy nhất, ổn định ở mỗi ván. Đây là dấu hiệu cần quay lại nhìn cấu trúc dữ liệu thay vì tiếp tục tăng depth.

Điểm bất thường có ích thực sự là quỹ đạo của hậu trắng.

## Vì sao chọn kỹ thuật vẽ quỹ đạo?

- Mỗi ván có nhiều nước hậu trắng hơn hẳn một ván bình thường.
- Phần lớn các ô đích kề nhau theo đường ngang, dọc hoặc chéo, giống nét bút.
- Có 24 ván, rất phù hợp để mã hóa một câu ngắn 24 chữ cái.
- Khi nối các tọa độ, ván đầu tạo chữ `H` rõ ràng; các ván tiếp theo tạo `A`, `R`, `D`.

Do đó, “chơi cờ hay dở” chỉ là lớp ngụy trang; tọa độ nước đi mới là dữ liệu.

## Các bước giải

1. Tách từng game từ PGN.
2. Trong mỗi số nước, chỉ lấy SAN của bên Trắng.
3. Giữ các token bắt đầu bằng `Q`.
4. Lấy ô đích cuối token, kể cả các dạng có `x`, `+` hoặc `#`.
5. Nối lần lượt các ô đích trên lưới 8×8.
6. Đọc 24 glyph theo thứ tự game.

Kết quả:

```text
H A R D  T O  K E E P  U P  W I T H  T H E  Q U E E N
```

Khoảng trắng được suy ra theo các từ tiếng Anh. Khi chuyển sang flag, thay khoảng trắng bằng dấu gạch dưới.

## Solver tối thiểu

Chạy từ thư mục `solve`:

```powershell
python .\render_queen_paths.py ..\files\games.pgn
```

Solver chỉ dùng thư viện chuẩn Python. Nó tạo:

- `queen_paths.svg`: montage 24 quỹ đạo để đọc chữ trực quan;
- `evidence.txt`: hash input, toàn bộ tọa độ, câu đã đọc và flag.

## Xác minh flag

Lượt xác minh từ đầu thực hiện trực tiếp trên file gốc và cho:

```text
Rendered 24 glyphs to queen_paths.svg
Decoded phrase: HARD TO KEEP UP WITH THE QUEEN
Flag: L3AK{HARD_TO_KEEP_UP_WITH_THE_QUEEN}
```

`evidence.txt` cũng xác nhận đủ 24 game và đúng SHA-256 của attachment. Vì flag bắt nguồn từ 24 glyph tái lập được, không phải suy đoán từ prompt, evidence là đủ để kết luận.

## Bài học và lỗi thường gặp

- Tên “Blunder” dễ khiến ta dùng engine quá lâu. Nếu kết quả engine không tạo quy luật nhất quán, hãy kiểm tra hình học của dữ liệu.
- Đừng chỉ trích ô đích rồi đọc chúng như ký tự ASCII; thứ tự tọa độ biểu diễn nét vẽ.
- Chỉ dùng nước hậu trắng. Thêm điểm xuất phát `d1` hoặc nước của quân khác sẽ tạo nét thừa.
- SAN có thể chứa `x`, `+`, `#`; regex phải lấy ô đích ở cuối token thay vì cắt chuỗi ở vị trí cố định.
- Giữ thứ tự ván trong PGN vì đó chính là thứ tự ký tự.
