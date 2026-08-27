# Evidence manifest

## `calibrated_radiograph.png`

- **Claim supported:** 617 nhóm projection tạo thành một volume có tấm chữ 3D;
  longitudinal radiograph sau hiệu chỉnh spacing hiển thị
  `L3AK{CT_Sc4Ns_R_JU57_L0tz_0F_Xr4y5!!!}`.
- **Source/tool:** `files/scan2.7z` -> `scan2.sqlite`; `solve/solve.py` dùng
  SQLite, NumPy và Pillow.
- **Reproduction command:**

  ```powershell
  python ".\Forensics\You Scanned HOW_!_!\solve\solve.py" `
    ".\Forensics\You Scanned HOW_!_!\files\scan2.7z" `
    ".\Forensics\You Scanned HOW_!_!\solve\evidence\calibrated_radiograph.png"
  ```

- **Input SHA-256 (`scan2.7z`):**
  `7f1ee82b27d7d7a5886703e26082fde58705f4272b38c09ad0943d5f3e1e598c`
- **Extracted SQLite SHA-256:**
  `626ea7fd01761cc448abb95823d4e3f91f6e1fcaad792db4a98362bba448c3c8`
- **Evidence SHA-256:**
  `354c5578d38b5efd4e32094a5c3d15875a1be445ca9c77b24cee87dfd4b76004`
- **Why retained:** đây là output nhỏ duy nhất chứng minh representation 3D,
  phép hiệu chỉnh hình học và từng ký tự của flag.

## Verification replay

Hai lần chạy solver độc lập từ archive gốc đều đọc 617 slice, suy ra spacing 3,
tính PCA angle `79.126338°` và tạo PNG có cùng SHA-256
`354c5578d38b5efd4e32094a5c3d15875a1be445ca9c77b24cee87dfd4b76004`.
File replay tạm không được giữ lại.
