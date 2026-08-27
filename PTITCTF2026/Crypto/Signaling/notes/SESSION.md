# Signaling — session

## Restate
Video `Signaling.mp4` (553 frames, 1080×1350, 25fps). Flag `PTITCTF{...}`.
Previous agents treated it as a lighthouse; it is a **clock** (hands + 8 outer sectors that light in pairs).

## What is in the video
- Inner analog clock with 2 white hands and ticks at 12/3/6/9.
- Outer ring of **8 sectors**; typically **2 sectors** are highlighted.
- Hands move in ~7–10 frame holds (semaphore-like).

## Signals extracted
1. Outer 2-of-8 sector pairs (`solve/out/clock_fast.json`) — 42 symbols, 24 unique pairs.
2. Inner-hand angles via bright-pixel histogram (`solve/out/hands.json`) — ticks at 3/12 contaminate peaks; r=70–130 still misses some hands (e.g. f300 3 o’clock).
3. Upper-frame brightness Morse (`EIUEE ...... EEE NA EE`) is likely an artifact of which sectors enter the crop, not a real Morse plaintext.

## Decode attempts
- Flag semaphore on sector pairs, 8 rotations × mirror, scout/Wikipedia tables: no `PTIT`.
- Same on hand pairs: no `PTIT` (hand extraction still noisy).
- 6-bit `(a<<3)|b` as ASCII/base64: no `PTIT`.
- Prefix equality pattern for `PTITCTF` (T repeats) does not match the sector sequence at any offset.

## Next (ranked)
1. Recover the rule relating the 47 ordered hand symbols to the first 42 real outer-sector symbols. Direct XOR/add/subtract, angular offsets, fixed pairing, Vigenere-on-letter-indices, and fixed lag/permutation have been ruled out.
2. Inspect the original ABM `次元通信 (Signaling)` MV or creator notes for the exact two-channel semaphore convention; external search confirmed that the MV intentionally contains semaphore and hidden messages, but did not yield a decode.
3. If no convention is found, model the outer pair as a per-symbol dihedral reference frame and search only transformations constrained by English/`PTITCTF` structure.

## 2026-08-22 checkpoint
- Correct center is `(540, 675)` for ray sampling.
- The clock hands have distinct lengths: long hand ends at radius about 164 px, short hand at about 114 px; static cardinal ticks start around radius 171 px.
- Sampling the middle of each 10-frame hold gives 47 ordered `(long, short)` symbols. A single global transform (rotate +45 degrees and mirror) maps every pair to a valid standard semaphore letter:
  `HWRNUQZQKJEXRMUWBKRIUPFCRMUJHNXWMRLNHUCVOTMOLRK`
- The outer ring contains 42 real two-sector symbols. It is not a simple delayed or permuted copy of the hands.
- Ruled out: MP4 appended/text payload, obvious H.264 LSB stream, direct semaphore plaintext, 6-bit XOR/add/subtract, coordinate-wise angular compensation, cross-pairing hands with sectors, obvious keyword Vigenere, and fixed-lag matching.
- Flag status remains **none**; do not create `final_flag.txt`.

## Files
- `solve/clock_fast.py`, `hands_hist.py`, `sema_hands.py`, `sema2.py`, `bits6.py`
- `solve/out/*.png` sample frames

## 2026-08-22 — hướng mới (chưa thử, ưu tiên cao)
Đã xác nhận: 2 kênh đều là "2 vị trí trong 8 hướng" (semaphore 2 cánh). Bảng semaphore chuẩn + 8 rotation × mirror trên KÊNH KIM đều ra gibberish (no PTIT).

**Nghi ngờ chính: EXTRACTION sai, không phải cần lớp-2.** 154pts crypto → 1 kênh nên ra thẳng flag.
1. **Hoán long/short = trái/phải cánh tay.** Semaphore phân biệt tay trái vs phải; nếu gán nhầm kim dài/ngắn thì MỌI letter sai. Thử decode với (short,long) thay vì (long,short), lại 8 rot × mirror.
2. **Center/mapping vị trí lệch.** clock_fast center=[553,673], hands dùng [540,675]. Chuẩn hoá 1 center, re-quantize góc → 8 hướng, verify bằng frame 300 (kim ở 12 & 3 = phải map ra letter cụ thể).
3. **Kênh vòng ngoài = rotating reference frame (per-symbol).** Align 2 kênh THEO FRAME (không theo index): tại mỗi symbol, sector vòng ngoài = hướng "Bắc" hiện tại → xoay cặp kim theo sector rồi tra bảng. Prior chỉ thử offset góc TOÀN CỤC, chưa thử per-symbol.
4. "Roblox" hint: tên "Signaling" = RemoteEvent/BindableEvent (signal) trong Roblox/Luau — nhiều khả năng chỉ xác nhận "đây là semaphore cờ tay hàng hải", không phải lớp mã hoá thêm. Ưu tiên #1/#2 trước.

Không có audio track (video-only, x264). MP4 không có payload đuôi.
