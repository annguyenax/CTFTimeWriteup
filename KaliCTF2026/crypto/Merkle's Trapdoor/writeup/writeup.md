# Merkle's Trapdoor

## Overview
- Category: Crypto
- Points: 100
- Author: F4R3S

## Solution
The challenge provides a ciphertext and a public key for a Merkle-Hellman Knapsack Cryptosystem. The public key has only 8 elements:
`{14, 5937, 140, 213, 3, 1403, 901, 2009}`

Since the block size is only 8 bits (1 byte) and the public key has 8 elements, the number of possible plaintext blocks is 2^8 = 256. This means we can completely bypass the need for a private key or LLL by simply brute-forcing all 256 possibilities for each block.

By iterating through all 256 possible 8-bit values, multiplying the bits (LSB first) by the public key elements, and matching the sum to each ciphertext block, we can instantly decrypt the flag.

## Flag
`KaliTeam{M4rK14_h3lLm3n_Kn3ps3cK}`