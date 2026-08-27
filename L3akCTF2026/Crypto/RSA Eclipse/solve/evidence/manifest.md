# Evidence manifest — RSA Eclipse

| File | Claim supported | Source/tool | Reproduction | Why kept |
|---|---|---|---|---|
| output.txt | N, e, c công khai | trong `files/crypto_rsa-eclipse.tar.gz` | `tar -xzf files/...` | Đầu vào solver |
| ../solve.py | Khôi phục p,q từ cấu trúc N rồi giải RSA | Python | `python solve/solve.py` | Solver xác định |

## Kết quả xác minh

- `python solve/solve.py` → `a=2799, b=1749`, `p*q == N: True`, flag:
  `L3AK{Th3_P3numbr4_H1d35_Th3_Fl4w_In_Th3_Mers3nne_V01d}`
- **Verify mạnh:** `p*q == N` đúng chính xác (không đoán) với `p=2^607−2799`, `q=2^521−1749`; flag giải ra ASCII sạch, đúng khung `L3AK{}`, nội dung có nghĩa ("penumbra hides the flaw in the Mersenne void").

Artifact gốc: `files/crypto_rsa-eclipse.tar.gz`
SHA-256: `b84b7e1d6c7f6b5d6dca558f7b9e0bae2d3f503f0ec228d2bb978a7e502c0c3e`
