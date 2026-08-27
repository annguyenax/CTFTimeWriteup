# Critical Flight — Writeup (HTB Try Out / Hardware) (Tiếng Việt)

## 1. Đề
Challenge hardware (very easy), file-only: `hw_critical_flight.zip`.
PCB KiCad “HadesMicro” dạng Gerber (`.gbr`): silk, mask, paste, 4 lớp đồng (F/In1/In2/B).
Mục tiêu: tìm chỗ saboteur giấu chữ trên bản mạch, flag `HTB{...}`.

## 2. Kiến thức nền
- **Gerber**: mô tả vector lớp PCB để sản xuất (đồng, silk, mask).
- **Silkscreen**: mực in ký hiệu linh kiện — hay bị soi trước, nhưng flag có thể nằm **dưới mask**, trên **đồng**.
- Cần raster hóa (pygerber) rồi đọc từng lớp, xoay/lật vì text có thể xoay 90°.

## 3. Phân tích
- Không có chuỗi `HTB` trong text Gerber (chữ là aperture/stroke).
- Silk top/bot: nhãn chân `TX/RX`, `HADES micro` — không flag.
- `HadesMicro-B_Cu.gbr` (đồng đáy): vùng đồng khoét chữ
  `HTB{533_7h3_1nn32_w02k1n95` (xoay 90°, đọc qua ảnh đã rotate).
- `HadesMicro-In1_Cu.gbr` (đồng trong L2):
  `_0f_313c720n1c5#$@}`

## 4. Vì sao hướng này
- H1 flag trên silk → render F/B silkscreen: không có HTB, kill.
- H2 flag trên đồng ngoài/trong: B_Cu + In1_Cu khớp hai nửa một flag.
- H3 In2/F_Cu: không text flag.

## 5. Các bước
1. Giải nén zip → `flight_control_board/*.gbr`.
2. `pygerber` raster `B_Cu` và `In1_Cu` (dpmm=40).
3. Xoay B_Cu 90° để đọc nửa đầu (text bị mirror/rotate).
4. Nối hai nửa. Hai lớp độc lập cùng một chuỗi.

```text
python solve/solve.py
```

## 6. Flag
```
HTB{533_7h3_1nn32_w02k1n95_0f_313c720n1c5#$@}
```
