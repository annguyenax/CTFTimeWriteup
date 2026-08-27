# Dynamic Paths

## 1. Tổng quan

- **Loại:** coding
- **Độ khó:** easy
- **Tác giả:** makelaris
- **Mô tả:** Bạn đang ở trong mạng lưới đường hầm ngầm và bị một con behemoth đột biến truy đuổi. Bạn có bản đồ các khu vực (grid) với khoảng cách giữa các khối. Cần tìm đường đi tối ưu từ góc trên bên trái đến góc dưới bên phải, chỉ được đi **xuống hoặc sang phải**, sao cho tổng các số đi qua là **nhỏ nhất**, để thoát khỏi behemoth.
- **Mục tiêu:** Trả lời đúng 100 bài test (mỗi bài là một grid) để nhận flag.

## 2. Thông tin instance

- **Target (spawn mới nhất):** `154.57.164.78:30321` (TCP)
- (target.txt cũ ghi `154.57.164.66:32355` — instance đã được reset, port/host đổi.)
- Kết nối bằng `nc 154.57.164.78 30321`.

## 3. Phân tích giao thức

Server gửi banner mô tả bài toán và 100 test:

```
You will be given a number of t = 100 grids ...
	1. The dimensions i x j of the map grid where 2 <= i, j <= 100
	2. The numbers n_i,j symbolizing the distances between the blocks where 1 <= n_i,j <= 50
You will start at the top left element, and your goal is to reach the bottom right,
while only being allowed to move down or right, minimizing the sum of the numbers you pass.
```

Mỗi test có dạng:

```
Test 1/100
4 4
1 1 4 1 8 6 4 6 1 6 6 6 9 4 3 7
>
```

- Dòng đầu: kích thước `i j`
- Dòng tiếp theo: `i*j` số, theo thứ tự row-major
- Cần gửi lại tổng nhỏ nhất của đường đi.

Ví dụ server đưa ra: grid `4x3` `[2 5 1 / 9 2 3 / 9 1 3 / 11 7 4]` → đáp án `17` (đường `2→5→2→1→3→4`).

## 4. Giải thuật

**Minimum path sum — quy hoạch động (DP):**

- `dp[r][c]` = tổng nhỏ nhất để đến ô `(r, c)`.
- Ô xuất phát: `dp[0][0] = grid[0][0]`.
- Hàng đầu: `dp[0][c] = dp[0][c-1] + grid[0][c]`.
- Cột đầu: `dp[r][0] = dp[r-1][0] + grid[r][0]`.
- Còn lại: `dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])`.
- Đáp án: `dp[i-1][j-1]`.

Triển khai dùng mảng 1 chiều `dp[j]` (chỉ giữ dòng hiện tại) để tiết kiệm bộ nhớ — tối đa grid 100×100 nên không vấn đề gì.

Script `solve/solve.py`:
1. Kết nối socket tới server, đọc banner.
2. Với mỗi test: parse `i j` và `i*j` số từ buffer, chạy DP, gửi kết quả kèm `\n`.
3. Lặp 100 lần, đọc output cuối chứa flag.

## 5. Kết quả

- 100/100 test trả lời đúng (tổng nhỏ nhất của từng grid).
- Server trả về:

```
You managed to traverse the maze of the underground and escape the behemoth.
Here is your reward: HTB{b3h3M07H_5h0uld_H4v3_57ud13D_dYM4m1C_pr09r4mm1n9_70_C47ch_y0u_991d7f7b4f430cfd2a9b79af13d03203}
```

- **Flag:** `HTB{b3h3M07H_5h0uld_H4v3_57ud13D_dYM4m1C_pr09r4mm1n9_70_C47ch_y0u_991d7f7b4f430cfd2a9b79af13d03203}`

## 6. Bài học

- Dạng bài "minimum path sum" trên grid chỉ đi xuống/phải là DP kinh điển; parse dữ liệu từ socket cần chú ý buffer tích lũy (dữ liệu có thể đến nhiều chunk) và tách block theo `Test X/100 ... >`.
- Khi viết solver tương tác với server, nên đọc đến marker (`> `), reset buffer sau mỗi lượt, và kiểm tra đủ số lượng giá trị trước khi tính.
- Với bài coding CTF, luôn giữ kết nối socket trong suốt vòng lặp 100 test, không đóng/khởi tạo lại từng lần.
