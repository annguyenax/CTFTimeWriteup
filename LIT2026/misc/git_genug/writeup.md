# git_genug

## Overview
A simple git forensics challenge. We are given a git repository and told a secret was leaked but cleaned up.

## Solution
1. Checking `git log --all --stat` showed a fake flag in a commit.
2. Checking `git reflog` revealed an unreferenced commit `e5ed944` that was removed via `git reset`.
3. Running `git show e5ed944` revealed the real flag in `secret.txt`.

**Flag:** `LITCTF{r3fl0g_1s_y0ur_g1t_t1m3_m4ch1n3}`
