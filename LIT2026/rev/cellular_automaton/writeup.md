# cellular_automaton

## Overview
The challenge gives us an ELF binary and a hex string representing the output of running a cellular automaton on the flag.

## Analysis
Looking at the disassembly, the program converts the 26-byte input flag into 208 bits. It then applies a Rule 90 cellular automaton on this bit array for 32 steps.

Specifically, for each step, it updates the array according to:

ew_array[i] = array[(i-1)%208] ^ array[(i+1)%208]

After 32 steps, it compares the output with the hardcoded bytes.
Because the transformation is purely XOR operations over bits, it is linear over GF(2) and can be represented as a matrix multiplication M * x = b.

By building the transition matrix M corresponding to 32 steps of Rule 90, we get:
M[i, (i - 32) % 208] = 1
M[i, (i + 32) % 208] = 1

## Solution
We construct the matrix M and try to solve the linear system over GF(2). 
The matrix is not fully invertible (it has a nullity of 16). This means there are ^{16}$ possible preimages. 
By searching the null space for a solution that begins with the known flag prefix LITCTF{, we can uniquely identify the correct flag.

**Flag:** LITCTF{g0ing_b4ck_1n_t1m3}
