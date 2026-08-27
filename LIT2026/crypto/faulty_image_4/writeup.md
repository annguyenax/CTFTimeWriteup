# faulty_image_4

## Solution
The challenge provides an image `corrupt4.png`. The description hints that some pixels were corrupted and separated from encoding information as a whole. A further hint points out that some pixels have unusually small blue values, almost like they've been clipped to 4 bits.

By examining the image pixels, we find that on the first row (y=0), there are 54 pixels with blue values $\le 15$ (which fits in a 4-bit nibble). 

By extracting these 54 blue values and grouping them into pairs of two (combining two 4-bit nibbles into one 8-bit byte), we decode the hidden flag.

## Flag
`LITCTF{pr1m3_n1bbl3s_77zq!}`
