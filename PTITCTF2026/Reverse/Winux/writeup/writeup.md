# Winux — Reverse (PTITCTF2026)

**Flag:** `PTITCTF{50m371m35_my_c011346u35_pr3f3r_u51n6_11nux_0v3r_w1nd0w5}`
("sometimes my colleagues prefer using linux over windows")

## Files
- `winux.exe` — fake Linux (install → login → shell), loads `lib/winuxsvc.dll` (WUX2 rootfs) + `lib/libpam_w32.dll` (PAM auth).
- `rootfs.wux` — custom "WUX2" encrypted filesystem (592B) holding flag.txt, real_password, etc.

## Solve
1. Run `winux.exe`. Installer asks Username + Password (6-32 printable, no spaces), then drops to a shell.
2. `cat flag.txt` in the user home returns a DECOY:
   `PTITCTF{w1nd0w5_4nd_11nux_4r3_4_p41r_7h47_pr06r355_70637h3r}6546`
   The trailing `6546` (a "corrupted package key" marker) makes it invalid.
3. `/root` is "Permission denied! **Try running as Administrator**" — the Winux trick:
   winux checks the **Windows process token elevation**. Run `winux.exe` **as Administrator**:
   > "Windows Administrator token detected. Starting root recovery shell."  → uid=0(root)
4. `cat /root/flag.txt` → the real flag.

## Reproduce (Windows)
```
del winux.state
# as Administrator:
winux.exe   # install any user/pass, then: cat /root/flag.txt
```
`/root/real_password` = 0d4d7ec31ea831cd17e8edf5c4161d85183f7cc203360cbf616c2841dfe3b674 (sha256 of login pw; not needed).
