import re
# Try to decode UART from _exp.bin treating each byte as a sample.
# UART 8N1 @ 115200, sample rate 25MHz => samples per bit = 25000000/115200 = 217
# Determine high/low from byte value.
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\hw\Debug\files\_work\sal_extracted\digital-1_exp.bin", 'rb').read()
print("len", len(data))

def decode(rate_hz, spb, high_test, name):
    # build bit array
    bits = [1 if high_test(b) else 0 for b in data]
    # We need sample index per sample: each byte = 1 sample.
    # UART: idle high. Start bit = low (0). 8 data bits LSB first, stop high.
    # Sample at mid-bit: index = start_idx + 1.5*spb etc. Simpler: detect start (high->low),
    # then sample at spb increments.
    result = []
    i = 0
    n = len(bits)
    while i < n - spb*10:
        if bits[i] == 1:  # high, wait for start (falling edge)
            i += 1
            continue
        # potential start bit at i (low). Check it's a real start: previous high
        if i > 0 and bits[i-1] != 1:
            i += 1
            continue
        # sample data bits at mid positions
        byte = 0
        ok = True
        for b in range(8):
            pos = i + int(spb * (1.5 + b))
            if pos >= n:
                ok = False; break
            bitval = bits[pos]
            byte |= bitval << b
        if ok:
            stop_pos = i + int(spb * (9.5))
            if stop_pos < n and bits[stop_pos] == 1:
                result.append(byte)
        # advance past this frame
        i += int(spb * 10)
    txt = bytes(result).decode('latin1')
    print("=== %s (spb=%d) decoded %d bytes ===" % (name, spb, len(result)))
    print(txt[:1500])
    return txt

# Try: high = byte in {255, 1}? Let's detect value set
from collections import Counter
c = Counter(data[:100000])
print("sample values in first 100k:", c.most_common(6))

# high test: byte >= 0x80
decode(25000000, 217, lambda b: b >= 0x80, "thresh128")
# high test: byte != 0
decode(25000000, 217, lambda b: b != 0, "nonzero")
