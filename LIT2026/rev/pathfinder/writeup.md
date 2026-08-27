# pathfinder

## Overview
The binary checks our input which must be a balanced parenthesis sequence of length 70 (35 open, 35 closed). 
It then calculates a "score" for our sequence and expects it to equal exactly `1337133713371337133` (which is `0x128e740722b291ad` in hex).

## Analysis
By analyzing the assembly, the binary first computes a 36x36 DP table (`grid[i][j]`) that stores the number of valid parenthesis sequences starting from a prefix with `i` open parentheses and `j` closed parentheses.
During the checking phase, for every `)` character in our string, it adds the number of valid sequences that would have been formed if we had placed a `(` instead. 
This is exactly the unranking algorithm to find the 0-based lexicographical index of a balanced parenthesis sequence.

The binary expects the lexicographical index to be `0x128e740722b291ad`.

## Solution
We can recreate the DP table to count valid parenthesis sequences and use the standard unranking algorithm to find the 0x128e740722b291ad-th valid balanced parenthesis sequence of length 70.

```python
grid = [[0 for _ in range(36)] for _ in range(36)]

for num_open in range(35, -1, -1):
    for num_close in range(35, -1, -1):
        if num_open < num_close:
            grid[num_open][num_close] = 0
        elif num_open == 35 and num_close == 35:
            grid[num_open][num_close] = 1
        else:
            val = 0
            if num_open < 35:
                val += grid[num_open+1][num_close]
            if num_close < 35 and num_open >= num_close + 1:
                val += grid[num_open][num_close+1]
            grid[num_open][num_close] = val

target = 0x128e740722b291ad
result = ""
num_open = 0
num_close = 0

for i in range(70):
    if num_open < 35:
        num_ways_if_open = grid[num_open + 1][num_close]
    else:
        num_ways_if_open = 0
        
    if target < num_ways_if_open:
        result += "("
        num_open += 1
    else:
        result += ")"
        target -= num_ways_if_open
        num_close += 1

print("Flag: LITCTF{" + result + "}")
```

**Flag:** `LITCTF{((())((()))())(((()())))(()(()((((()())))))((()((())((())(()))))(())))}`
