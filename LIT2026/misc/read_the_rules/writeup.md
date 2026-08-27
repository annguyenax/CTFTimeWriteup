# read_the_rules

## Solution
The challenge provides a GIF `grid.gif` showing the evolution of a 64x64 Cellular Automaton over 64 frames. It also gives `permutation.txt`, which contains a permutation of numbers from 0 to 255.
The description states: "Each cell's next state only depends on the state of its 8 neighboring cells, and the edges wrap back to the other side. He also said there's a secret message and gave me this list".

By analyzing the first two frames of `grid.gif`, we can extract the CA transition truth table (since there are exactly 256 unique 8-neighbor configurations present, and no conflicts).
This truth table maps an 8-bit neighbor configuration to a 1-bit next state, which gives 256 bits of data. 

The permutation in `permutation.txt` is the key. By brute-forcing the 40,320 possible neighbor reading orderings, we can find the correct order that forms the 8-bit integer for each neighborhood. We then apply the `permutation.txt` to the 256 bits of the transition truth table, and decode the bits to ASCII bytes.

One of the reading orderings successfully decodes to a string containing the flag.

## Flag
`LITCTF{th3_fl4g_1s_in_th3_ru1e5}`
