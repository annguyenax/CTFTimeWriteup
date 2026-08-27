# Evidence manifest — faulty_image_3

| File | Claim supported | Source/Tool | Reproduction | Why kept |
|------|-----------------|-------------|--------------|----------|
| ../solve.py | Real flag = RED channel of the 30 top-border marks | solver | `python solve/solve.py files/corrupt3.png` | Reproduces real flag |
| border_marks.png | The top orange border has blue-ish marks every 7px (the hidden data) | PIL crop/zoom | zoom a[0:6,:220] | Shows the encoding |
| rendered.png | Full image render (orange frame + red DECOY text) | PIL | open corrupt3.png | Shows decoy |
| flag_zoom.png | Zoom of the red DECOY text `LITCTF{1mAg3_F1ag_1o3fjs!}` | PIL | — | Documents the decoy |

## Result
- corrupt3.png sha256 = f92cedbd46bc1c7c2498993164659d7ba88cfb18b18e67577bc87a2d25b43006
- Visible red text `LITCTF{1mAg3_F1ag_1o3fjs!}` is a **DECOY**.
- Real flag hidden on the top border (y=0): 30 pixels spaced every 7px, colored
  differently from the orange border. Their **RED channel** = the flag; G/B are
  noise so the marks just look "colorful".
- **Flag: `LITCTF{p1x3l_p3rf3ct_98xzfq9!}`**  ("pixel perfect")

## Verification
`python solve/solve.py` deterministically reads the 30 marks' red channel and
prints `LITCTF{p1x3l_p3rf3ct_98xzfq9!}` (30 chars, LITCTF{...} well-formed).
