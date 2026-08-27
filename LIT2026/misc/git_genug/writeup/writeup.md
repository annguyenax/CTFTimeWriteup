# git genug - LIT CTF 2026 (Misc)

## 1. Yêu cầu bài toán
Đề bài cho biết họ đã vô tình để lộ (leak) một thông tin bí mật trong kho lưu trữ Git (repo) này, nhưng họ nghĩ rằng đã dọn dẹp sạch sẽ trước khi push. Mục tiêu là chứng minh họ sai bằng cách tìm ra secret (cờ) đã bị xóa.

## 2. Kiến thức nền tảng
- **Git Forensics**: Phân tích lịch sử thay đổi của Git.
- **Git Reflog**: Mọi hoạt động làm thay đổi HEAD trong Git (kể cả việc reset, xóa commit, amend) đều được lưu lại trong git reflog. Dù một commit không còn nằm trong lịch sử git log chính thức, nó vẫn có thể được truy xuất thông qua eflog.

## 3. Quá trình phân tích & Giải
- Sau khi giải nén file gitgenug.zip, ta thấy một thư mục epo chứa một kho Git hợp lệ.
- Lệnh git log thông thường không cho thấy bất kỳ dấu vết nào của cờ.
- Chạy lệnh git reflog để xem toàn bộ lịch sử thao tác HEAD. Ta phát hiện hai commit đáng ngờ:
  - 2cad4d5: "WIP flag stuff (probably not needed)"
  - e5ed944: "Add local dev notes (oops, forgot to gitignore)"
- Khi dùng lệnh git show 2cad4d5, ta thu được một fake flag (cờ giả): LITCTF{n0t_th3_r34l_fl4g_k33p_l00k1ng}
- Tiếp tục kiểm tra commit thứ hai bằng lệnh git show e5ed944, ta thấy nội dung file secret.txt chứa cờ thật sự.

## 4. Bằng chứng (Evidence) & Lệnh tối thiểu
- Lưu solve.sh ghi lại các lệnh cần thiết:
  `ash
  unzip gitgenug.zip
  cd repo
  git reflog
  git show e5ed944
  `

## 5. Xác minh Flag
- Flag: LITCTF{r3fl0g_1s_y0ur_g1t_t1m3_m4ch1n3}

## 6. Bài học rút ra
Trong Git, việc sử dụng git reset --hard hay xóa file rồi tạo commit mới KHÔNG làm mất đi dữ liệu ngay lập tức. Dữ liệu vẫn được lưu trữ tạm thời và hoàn toàn có thể khôi phục dễ dàng bằng git reflog.
