# Stranger Papers

- **Event:** PTITCTF 2026
- **Category:** Crypto
- **Points:** 500
- **Flag format:** `PTITCTF{...}`

## Prompt (verbatim)

> [PHÒNG THÍ NGHIỆM HAWKINS - TỐI MẬT] — 6/11/1983. Project "Stranger Papers".
> The Sector-4 signal is lost. The researchers left an encrypted document before the power failed.
> These pages are rumoured to hold the unique coordinates linking our world and The Upside Down.
> Something leaked from the void and distorted the data. Decode it before the Mind Flayer finds you.

## Recon

`files/Stranger Papers.zip` (269 MB) expands to **502 photos** (`1.jpg` … `502`), a mix of
**455 `.jpg`** and **47 `.HEIC`**. Hashing them by content leaves only **22 unique images**.
Reading the files in filename order and assigning each unique image a symbol gives a
**502-symbol sequence over a 22-letter alphabet** (`notes/seq.txt`, labels `A`=U00 … `V`=U21).

Each unique image is a large handwritten letter/digit drawn on a sheet and then **folded
(blintz)**, so only stroke fragments at the four corners are visible — hence "something leaked
from the void (the fold hides the middle) and distorted (fragmented) the data". The sequence of
folded glyphs is a **monoalphabetic substitution cipher**.

## The wrong turn that cost most of the time

The prior assumption was *English*. But:

- IC = **0.078**, clearly above English prose (0.066) — too concentrated.
- Every English quadgram / dictionary / quipqiup-style attack collapses into a
  spurious `AND…AND…AND` local optimum; the true plaintext is unreachable.
- The glyph count (**22**) is exactly the **Vietnamese alphabet without diacritics**
  (`a b c d e g h i k l m n o p q r s t u v x y` — no `f j w z`), and the frequency profile
  (top two symbols ≈ 13–14 %, then a long tail) matches Vietnamese, where `a`/`n` dominate.

So the document is **Vietnamese** (spaces removed, diacritics stripped), not English.

## Solve

Build a Vietnamese character-quadgram model (scrape `vi.wikipedia.org`, strip diacritics to the
22-letter alphabet) and simulated-anneal the substitution exactly like an English quadgram cracker
(`solve/solve.py`). It converges to a coherent paragraph:

```
giua long ha noi on ao mot khoang san gach co van lang le duoi nhung tan cay xanh mat
ngoi reu phong cong tam quan gieng nuoc vuon va khue van cac thanh nha khien nguoi ta
nhu buoc vao mien ky uc xa xua nhung tam bia tren lung rua da ghi ten cac bac hien tai
nhac rang tri thuc la nen mong cua quoc gia noi ay khong chi luu giu bong dang mot truong
hoc co ma con goi niem tu hao ve truyen thong hieu hoc cua dan toc moi buoc chan qua day
deu goi len hinh anh nhung si tu den sach mang theo uoc vong doi thay cuoc doi va dem tai
nang phung su dat nuoc giua nhip song khong gian ay van tram mac nhac rang hoc van va dao
duc luon la hanh trang quy gia
```

With diacritics restored:

> Giữa lòng Hà Nội ồn ào, một khoảng sân gạch cổ vẫn lặng lẽ dưới những tán cây xanh mát.
> Ngôi rêu phong, cổng tam quan, giếng nước, vườn và **Khuê Văn Các** thanh nhã khiến người ta
> như bước vào miền ký ức xa xưa. Những tấm **bia trên lưng rùa** đã ghi tên các bậc hiền tài,
> nhắc rằng tri thức là nền móng của quốc gia. Nơi ấy không chỉ lưu giữ bóng dáng một trường học
> cổ mà còn gợi niềm tự hào về truyền thống **hiếu học** của dân tộc…

The landmarks — *Khuê Văn Các*, the *turtle steles*, the *three-entrance gate*, *first university of
Vietnam* — identify the place unambiguously as **Văn Miếu – Quốc Tử Giám** (Temple of Literature,
Hà Nội). The "coordinates" the prompt asks for are those of Văn Miếu:

- **21.0286° N, 105.8356° E**

## Flag

```text
PTITCTF{21.0286_105.8356}
```

## Notes / verification

- Decryption is deterministic and reproducible (`solve/solve.py` converges to the same Vietnamese
  text across restarts); the paragraph is grammatically coherent and the landmark phrases are exact.
- The two EXIF GPS clusters found in the photos (21.2792,105.7208 and 21.00845,105.81793) are the
  photographers' locations — red herrings.
- The folded glyphs themselves never need to be read; the substitution is broken statistically.
