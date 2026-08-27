# kcufniarb

## Overview
We are given a string of symbols that resemble Brainfuck, but the challenge name is "kcufniarb" (Brainfuck spelled backwards). The string begins with `----------]`, which normally indicates the end of a loop.

## Solution
1. The code is written backwards both in syntax and logic.
2. By reading the string from right to left, we get a seemingly normal Brainfuck layout, but the characters have been reversed. 
3. Swapping all opposite instructions (e.g. `<` to `>`, `+` to `-`, `[` to `]`, `,` to `.`) gives a standard Brainfuck program.
4. Actually, reversing the string and swapping the characters isn't necessary if we just directly swap the characters on the left-to-right string. The original string `----------]<...` directly swapped becomes `++++++++++[>...` which is a valid Brainfuck script that prints out a flag.
5. Executing the valid script yields the flag.

**Flag:** `LITCTF{ti_did_ruoy_234rjwado4i3}`
