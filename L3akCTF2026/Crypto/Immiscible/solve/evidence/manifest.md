# Evidence manifest — Immiscible

| File | Claim supported | Source/tool | Reproduction | Why kept |
|---|---|---|---|---|
| ../public.json | Public key (9 đa thức bậc-2), target, encrypted_flag | challenge output | `python solve/solve.py` | Đầu vào solver |
| ../../files/crypto_immiscible/chal.py | Cấu trúc OV: quad chỉ có vinegar×vinegar và vinegar×oil (KHÔNG oil×oil) | archive gốc | đọc source | Chứng minh điểm yếu |
| ../solve.py | Brute vinegar → tuyến tính theo oil → khôi phục signature → giải AES | numpy | `python solve/solve.py` | Solver xác định (không cần z3/sage) |

## Kết quả xác minh

- `python solve/solve.py` (~48s) → `signature = [23,7,73,60,34,54,53,7]`, `eval==target: True`, flag:
  `L3AK{Oil_4ND_v1N3g4r_WitH0ut_Mix1nG_Sp1LL5_eV3rYth1ng}`
- **Verify mạnh:** signature thỏa **cả 9 phương trình công khai** (`eval_public(sig)==target`), và AES key = sha256(signature) giải ra flag unpad sạch, đúng khung `L3AK{}`, nội dung có nghĩa.

Artifact gốc: `files/crypto_immiscible.tar.gz`
SHA-256: `2987ea3c73f7efea24405de6c8b54925c7d446dd9c38e62b72d4494a2d277e9f`
