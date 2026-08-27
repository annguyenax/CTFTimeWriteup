# Evidence manifest

## `reconstruction.png`

- **Claim supported:** 180 projection trong SQLite tái dựng thành ảnh có chuỗi
  `L3AK{X-r4Y_C0mp13T3}`; hai dấu chấm than nằm ngoài dấu `}`.
- **Source/tool:** `files/scan.7z` -> `scan.sqlite`; `solve/solve.py` dùng SQLite,
  NumPy và `skimage.transform.iradon`.
- **Reproduction command:**

  ```powershell
  python ".\Forensics\You Scanned WHAT_!_\solve\solve.py" `
    ".\Forensics\You Scanned WHAT_!_\files\scan.7z" `
    ".\Forensics\You Scanned WHAT_!_\solve\evidence\reconstruction.png"
  ```

- **Input SHA-256 (`scan.7z`):**
  `e45a1da91290e654002c5c1ea49e5bf3caaad0e073dd76d848c2c2b6b955a92c`
- **Evidence SHA-256:**
  `aabee2bc31d0fca483346ed663ce37e9ecfd2d8b2fff8fc7cabd7bfd9cf2fdba`
- **Why retained:** đây là output nhỏ duy nhất cho phép người đọc kiểm tra trực quan
  vật thể được scan và từng ký tự của flag.

## Verification replay

Chạy solver lần thứ hai từ chính archive gốc vào một đường dẫn tạm tạo ra PNG có
cùng SHA-256
`aabee2bc31d0fca483346ed663ce37e9ecfd2d8b2fff8fc7cabd7bfd9cf2fdba`.
File replay là artefact dùng một lần nên không giữ trong repo.
