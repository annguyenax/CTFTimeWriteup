# Evidence manifest — BabyLCG

| File | Claim supported | Source/tool | Reproduction | SHA-256 | Why kept |
|---|---|---|---|---|---|
| chall.py | LCG cấu trúc: `state = (a*state + c) % m`, key = next output, ct = flag ^ key | Trong `files/beginner_baby-lcg.tar.gz` | `tar -xzf files/beginner_baby-lcg.tar.gz` | (xem gốc) | Chứng minh thuật toán mã hóa |
| output.txt | Giá trị công khai m, s0, s1, s2, ct dùng để khôi phục a, c, key | Trong archive | như trên | (xem gốc) | Đầu vào của solver |

## Kết quả xác minh

- `python solve/solve.py` → `L3AK{n3v3r_trU5t_b4s1c_LCG5_frfr}`
- Hai assertion hồi quy LCG (`a*s0+c ≡ s1`, `a*s1+c ≡ s2`) đều pass → tham số a, c đúng, không phải đoán.
- Flag giải ra là ASCII sạch, đúng tiền tố `L3AK{` và hậu tố `}`, dài 33 byte khớp độ dài placeholder `FLAG` trong chall.py.

Artifact gốc: `files/beginner_baby-lcg.tar.gz`
SHA-256: `d43183961f2cbbadcee66983f72c0c5c5548acb4b97784234ccc080d84ad6e8d`
