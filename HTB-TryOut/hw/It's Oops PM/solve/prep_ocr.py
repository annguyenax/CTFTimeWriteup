#!/usr/bin/env python3
import os
from PIL import Image, ImageOps, ImageFilter

SRC = r"D:\download\CTFTimeWriteup\HTB-TryOut\hw\It's Oops PM\files\_work\hardware_its_oops_pm\schematic.png"
OUT = r"D:\download\CTFTimeWriteup\HTB-TryOut\hw\It's Oops PM\solve\evidence"

im = Image.open(SRC).convert("L")
im2 = im.point(lambda p: 255 if p > 160 else 0)
im2 = im2.resize((im2.width * 2, im2.height * 2), Image.LANCZOS)
im2.save(os.path.join(OUT, "schematic_bw2x.png"))
print("saved bw2x", im2.size)

# invert for dark-on-white -> white-on-black? keep original orientation
im3 = ImageOps.invert(im2)
im3.save(os.path.join(OUT, "schematic_bw2x_inv.png"))
print("saved inv")
