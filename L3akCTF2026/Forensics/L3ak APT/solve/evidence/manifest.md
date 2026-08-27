# Evidence manifest

## `rizzler.jpg`

- **Claim supported:** Windows thumbnail cache còn giữ ảnh đã bị xóa khỏi
  `Downloads`; ảnh chứa chuỗi `L3AK{For3nsics_hUm4n$_C4n_c00K_AI}`.
- **Source/tool:** entry
  `C/Users/Max/AppData/Local/Microsoft/Windows/Explorer/thumbcache_1280.db`
  trong `files/L3AK_APT.zip`; `solve/solve.py` parse cấu trúc CMMM.
- **Cache hashes:** `15c78729be0524d8` và `237b7fe66e1c61d4`. Hai entry có
  payload JPEG byte-identical.
- **Reproduction command:**

  ```powershell
  python ".\Forensics\L3ak APT\solve\solve.py" `
    ".\Forensics\L3ak APT\files\L3AK_APT.zip" `
    ".\Forensics\L3ak APT\solve\evidence\rizzler.jpg"
  ```

- **Input SHA-256 (`L3AK_APT.zip`):**
  `e681d3bacaa0b8ad36715e6b355981201816341dcef11d0829f80a7ac46c5a98`
- **Evidence SHA-256:**
  `daa218b9d1713248f7069667ace2e21bcc46b42980e8b87c955ab1ec341701a2`
- **Why retained:** đây là payload quyết định duy nhất; nó cho phép kiểm tra trực
  quan nội dung đã khôi phục và từng ký tự của flag.

## Verification replay

Solver được chạy hai lần độc lập từ archive gốc. Cả output trong repo và output
tạm đều dài 185,015 byte và có cùng SHA-256
`daa218b9d1713248f7069667ace2e21bcc46b42980e8b87c955ab1ec341701a2`.
File replay tạm không được giữ lại.
