# Evidence manifest — me fr

| File | Claim supported | Source/tool | Reproduction | SHA-256 | Why kept |
|---|---|---|---|---|---|
| me_fr.txt | Ciphertext gõ lệch tay phải; decode ra đoạn văn tiếng Anh mạch lạc + flag | attachment gốc | `python solve/solve.py solve/evidence/me_fr.txt` | f927e41...7891a | Đầu vào duy nhất, chứng minh phép giải |

## Kết quả xác minh

- `python solve/solve.py` → decode toàn bộ thành:
  `Hi! So I was thinking... typing is just so hard nowadays! Looking at your hands while you type is infuriating, Anyways, heres the flag: L3AK{WHY_D0_1_dO_TH1S_s0_0f73N...}`
- **Verify mạnh:** cùng một bảng thế bàn phím (right-hand shift-left) giải nhất quán **cả câu văn tiếng Anh hợp lý lẫn flag** → không phải trùng hợp. Flag đúng khung `L3AK{}`, nội dung leetspeak có nghĩa "WHY DO I DO THIS SO OFTEN...".

Artifact gốc: `files/me_fr.txt` — SHA-256 `f927e419925139b6680de3884333dfb4dbdd0795b9a3ff6ae90f3d00b277891a`
