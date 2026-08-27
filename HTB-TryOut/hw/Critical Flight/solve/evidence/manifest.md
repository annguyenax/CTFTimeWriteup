# Critical Flight evidence manifest

| File | Claim | Source | Repro |
|------|-------|--------|-------|
| `HadesMicro-B_Cu.png` | First half `HTB{533_7h3_1nn32_w02k1n95` etched on bottom copper | Gerber `HadesMicro-B_Cu.gbr` | solve.py |
| `B_Cu_rot90.png` | Same text, rotated (mirrored) for reading | PIL rotate 90 | solve.py |
| `HadesMicro-In1_Cu.png` | Second half `_0f_313c720n1c5#$@}` on inner copper L2 | `HadesMicro-In1_Cu.gbr` | solve.py |

Flag = B_Cu + In1_Cu, read from our raster (not copied from a writeup).
