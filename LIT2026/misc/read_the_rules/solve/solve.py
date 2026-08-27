import itertools

# Reference rule extracted with ordering: NW, N, NE, W, E, SW, S, SE (0 to 7)
# MSB is NW (bit 7), LSB is SE (bit 0)
bits_str = '1001011011101000100001110011011010010101111100010100100000011110111001010100011011110011011011000001111010011010110001101111100100011100010011100001101001101110110001001110101111110010110011000100110001111000010100111110100011111010010110110010111110011100'
R_ref = [int(b) for b in bits_str]

with open('D:\\download\\CTFTimeWriteup\\LIT2026\\misc\\read_the_rules\\files\\permutation.txt') as f:
    perm = list(map(int, f.read().split()))

def try_decode(R_new):
    # Try p_type 0 and 1
    # p_type 0: p[i] = R_new[perm[i]]
    p0 = [0] * 256
    for i in range(256):
        p0[i] = R_new[perm[i]]
    s0 = ''.join(map(str, p0))
    res0 = ''.join(chr(int(s0[i:i+8], 2)) for i in range(0, 256, 8))
    if 'LITCTF' in res0:
        print('FOUND p0:', res0)
        
    # p_type 1: p[perm[i]] = R_new[i]
    p1 = [0] * 256
    for i in range(256):
        p1[perm[i]] = R_new[i]
    s1 = ''.join(map(str, p1))
    res1 = ''.join(chr(int(s1[i:i+8], 2)) for i in range(0, 256, 8))
    if 'LITCTF' in res1:
        print('FOUND p1:', res1)

print('Starting brute force of 40320 neighborhood orderings...')
# permutations of 0..7
for P in itertools.permutations(range(8)):
    # R_new[N_new] = R_ref[N_ref]
    R_new = [0] * 256
    for N_ref in range(256):
        # Extract bits of N_ref
        bits = [(N_ref >> i) & 1 for i in range(8)]
        # bits[0] is LSB, bits[7] is MSB.
        # In our ref, bit 7 is NW, bit 0 is SE.
        # Let's say bits_ref[i] = bit at position i.
        bits_ref = [(N_ref >> (7 - i)) & 1 for i in range(8)] # index 0 is NW
        
        # Permute bits according to P
        bits_new = [bits_ref[P[i]] for i in range(8)]
        
        # Form N_new
        N_new = 0
        for i, b in enumerate(bits_new):
            N_new |= (b << (7 - i))
            
        R_new[N_new] = R_ref[N_ref]
        
    try_decode(R_new)

print('Done.')
