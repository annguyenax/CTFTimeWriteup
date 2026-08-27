# Shush Protocol — Writeup (HTB Try Out / ICS) (Tiếng Việt)

## 1. Đề
Challenge ICS (very easy), file-only: `ics_shush_protocol.zip` → `traffic.pcapng` (thực ra là PCAP cổ điển magic `d4 c3 b2 a1`).
Mô tả: capture traffic máy chẩn đoán ↔ PLC, tìm packet chứa mật khẩu/secret.

## 2. Kiến thức nền
- **Modbus TCP** (IANA 502): ADU = Transaction ID (2) + Protocol ID (2, =0) + Length (2) + Unit ID (1) + Function (1) + data.
- Function chuẩn: `0x03` Read Holding Registers, `0x01` Read Coils.
- Function **≥ 65 (0x41)** thường là vendor-specific — đúng với “custom protocol” trong đề.
- File-only: flag nằm trong payload, không cần remote.

## 3. Phân tích
- 110 frame Ethernet/IPv4/TCP: `192.168.178.105` (HMI/diag) ↔ `192.168.178.23:502` (PLC).
- Định kỳ ~1s: FC `0x03` (đọc holding) và FC `0x01` (coils) — traffic “ồn”.
- Stream TCP `39888→502` dùng **FC `0x66` (102)**:
  - Poll lặp `66 00 47` (~100 ms).
  - Frame 34 (PLC→HMI): ASCII `operator`.
  - Frame 35 (HMI→PLC): `66 00 10` rồi `.HTB{50m371m35_cu570m_p2070c01_423_n07_3n0u9h7}`.

## 4. Vì sao hướng này
- H1 HTTP/FTP trong pcap: không có, toàn TCP/502 → Modbus.
- H2 đọc holding 0x03: payload toàn 0, không secret.
- H3 function lạ `0x66` + chuỗi `operator`/`HTB{` → đúng packet “secret information”.

## 5. Các bước
1. `strings` trên file → thấy `HTB{...}` (đường 1).
2. Parse PCAP: lọc TCP dport/sport 502, bóc Modbus ADU.
3. Frame 35, FC=0x66 chứa flag ASCII.
4. Hai đường (strings + parse ADU) cùng một chuỗi.

```text
python solve/solve.py
```

## 6. Flag
```
HTB{50m371m35_cu570m_p2070c01_423_n07_3n0u9h7}
```
