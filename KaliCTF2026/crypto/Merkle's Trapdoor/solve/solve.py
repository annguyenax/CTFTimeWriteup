import binascii

hex_ct = "1b99090e0a6109e30414099a090e0a6f211704f4060a20341b99058c060a1c2809d51cbd0a6104e60a6f1cbd21921c281b9921921cbd090320421cbd203f1b990a72"
pk = [14, 5937, 140, 213, 3, 1403, 901, 2009]

cts = [int(hex_ct[i:i+4], 16) for i in range(0, len(hex_ct), 4)]

# MSB first
flag1 = bytearray()
for ct in cts:
    for i in range(256):
        bits = [int(x) for x in bin(i)[2:].zfill(8)]
        if sum(bits[j] * pk[j] for j in range(8)) == ct:
            flag1.append(i)
            break
    else:
        flag1.append(63) # '?'

print("MSB:", flag1)

# LSB first
flag2 = bytearray()
for ct in cts:
    for i in range(256):
        bits = [int(x) for x in bin(i)[2:].zfill(8)][::-1]
        if sum(bits[j] * pk[j] for j in range(8)) == ct:
            flag2.append(i)
            break
    else:
        flag2.append(63)

print("LSB:", flag2)
