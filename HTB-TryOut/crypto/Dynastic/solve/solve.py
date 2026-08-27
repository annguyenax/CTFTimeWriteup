#!/usr/bin/env python3
"""Dynastic (HTB Try Out / crypto) — Trithemius (Caesar dịch theo vị trí)."""
c = "DJF_CTA_SWYH_NPDKK_MBZ_QPHTIGPMZY_KRZSQE?!_ZL_CN_PGLIMCU_YU_KJODME_RYGZXL"
p = "".join(chr((ord(x)-0x41 - i) % 26 + 0x41) if x.isalpha() else x
            for i, x in enumerate(c))
print("HTB{%s}" % p)
