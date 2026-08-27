data = '84ea cc57 4906 d24c cebd 93a2 3508 b04d 8b8f 8731 bc5a 0675 8a39 4143 b443 9ec3 030b b014 7066 5c34 2c18 b151 cb44 823d'.split()

extracted_bits = ''

for w in data:
    val = int(w, 16)
    # The 16 bits: index 0 to 15. Usually MSB is bit 0 or bit 15?
    # Let's assume standard left-to-right: MSB is bit 0 (overall parity), or maybe MSB is bit 15?
    # Let's test both. First, MSB is bit 0 (overall parity), bit 1 is P1, etc.
    # So val >> 15 is bit 0.
    bits = [(val >> (15 - i)) & 1 for i in range(16)]
    
    # Calculate syndrome
    p1 = bits[1] ^ bits[3] ^ bits[5] ^ bits[7] ^ bits[9] ^ bits[11] ^ bits[13] ^ bits[15]
    p2 = bits[2] ^ bits[3] ^ bits[6] ^ bits[7] ^ bits[10] ^ bits[11] ^ bits[14] ^ bits[15]
    p4 = bits[4] ^ bits[5] ^ bits[6] ^ bits[7] ^ bits[12] ^ bits[13] ^ bits[14] ^ bits[15]
    p8 = bits[8] ^ bits[9] ^ bits[10] ^ bits[11] ^ bits[12] ^ bits[13] ^ bits[14] ^ bits[15]
    
    error_pos = p8 * 8 + p4 * 4 + p2 * 2 + p1
    
    # Correct the error
    if error_pos != 0:
        bits[error_pos] ^= 1
        
    # Extract data bits
    d = [bits[3], bits[5], bits[6], bits[7], bits[9], bits[10], bits[11], bits[12], bits[13], bits[14], bits[15]]
    for bit in d:
        extracted_bits += str(bit)

flag = ''
for i in range(0, len(extracted_bits) - 7, 8):
    flag += chr(int(extracted_bits[i:i+8], 2))

print('MSB=0 Flag:', flag)
