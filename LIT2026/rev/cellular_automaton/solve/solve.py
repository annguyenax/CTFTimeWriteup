import numpy as np
import itertools

N = 208
M = np.zeros((N, N), dtype=int)
for i in range(N):
    M[i, (i - 32) % N] = 1
    M[i, (i + 32) % N] = 1

def rref(M):
    n, m = M.shape
    A = np.copy(M)
    row = 0
    for col in range(m):
        if row >= n: break
        pivot = -1
        for i in range(row, n):
            if A[i, col] == 1:
                pivot = i
                break
        if pivot == -1: continue
        A[[row, pivot]] = A[[pivot, row]]
        for i in range(n):
            if i != row and A[i, col] == 1:
                A[i] = (A[i] + A[row]) % 2
        row += 1
    return A, row

output_hex = "652b481a7c203a240b244f045b365f090016050e58227d270b37"
output_bytes = bytes.fromhex(output_hex)

def bytes_to_bits(b):
    bits = []
    for byte in b:
        for i in range(8):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_bytes(bits):
    b = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte |= (bits[i+j] << j)
        b.append(byte)
    return bytes(b)

output_bits = bytes_to_bits(output_bytes)

A = np.hstack((M, np.array(output_bits).reshape(-1, 1)))
A_rref, rank = rref(A)

pivots = []
row = 0
for col in range(N):
    if row < N and A_rref[row, col] == 1:
        pivots.append(col)
        row += 1

free_vars = [j for j in range(N) if j not in pivots]

flag_prefix = b'LITCTF{'
prefix_bits = bytes_to_bits(flag_prefix)

for free_vals in itertools.product([0, 1], repeat=len(free_vars)):
    sol = np.zeros(N, dtype=int)
    for i, var in enumerate(free_vars):
        sol[var] = free_vals[i]
        
    row = 0
    for j in range(N):
        if j in pivots:
            s = A_rref[row, -1]
            for f_var in free_vars:
                if A_rref[row, f_var] == 1:
                    s = (s + sol[f_var]) % 2
            sol[j] = s
            row += 1
            
    match = True
    for i in range(len(prefix_bits)):
        if sol[i] != prefix_bits[i]:
            match = False
            break
    if match:
        flag_bytes = bits_to_bytes(sol)
        print("Flag:", flag_bytes.decode())
        break
