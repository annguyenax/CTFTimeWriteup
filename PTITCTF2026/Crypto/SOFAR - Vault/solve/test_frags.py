#!/usr/bin/env python3
"""Test hypothesis: 8 fragments = 8 formations (position codes)."""
g = "0123456789bcdefghjkmnpqrstuvwxyz"
CROCK = {c:i for i,c in enumerate("0123456789ABCDEFGHJKMNPQRSTVWXYZ")}

def combine(frags):
    # frags: list of 8 equal-length strings
    out=[]
    for col in zip(*frags):
        x=0
        for c in col:
            x ^= (ord(c)&31)
        out.append(g[x])
    return "".join(out)

# Formations as list of position codes (read order matters).
# Let me define each formation's positions in various orders.
# Order A: top(ST)->bottom(GK), left->right per row
# F 4-4-2
F   = ["ST","ST","LM","RM","CM","CM","LB","RB","CB","CB","GK"]
R1  = ["ST","ST","LM","RM","CM","CM","LB","RB","CB","CB","GK"]
R2  = ["ST","ST","LM","RM","CM","CM","LB","RB","CB","CB","GK"]
QF  = ["ST","LW","RW","LM","RM","CM","LB","CB","CB","RB","GK"]   # 4-3-3 guess
SF  = ["ST","LW","RW","CM","CM","LWB","RWB","CB","CB","CB","GK"] # 3-4-3/3-5-2 guess
R3  = ["ST","ST","CAM","LM","RM","CM","CM","CB","CB","CB","GK"]
R16 = ["ST","ST","CM","CM","LWB","RWB","CB","CB","CB","GK"]      # 10 only
R32 = ["ST","ST","CAM","LM","RM","CM","CM","CB","CB","GK"]       # 10 only

frags = {
  "F":[F,R1,R2,QF,SF,R3,R16,R32],
}
def codes(f): return "".join(p for p in f)
# test various orders
def as_2char(fragments):
    return [codes(f) for f in fragments]

orders = {
 "top->bottom": [F,R1,R2,QF,SF,R3,R16,R32],
 "bottom->top": [f[::-1] for f in [F,R1,R2,QF,SF,R3,R16,R32]],
}
for oname, fraglist in orders.items():
    codes_lists = as_2char(fraglist)
    print("=== order:", oname, "===")
    for i,cl in enumerate(codes_lists):
        print(f"  frag{i+1}: len={len(cl)} {cl}")
    # check equal length
    lens=set(len(x) for x in codes_lists)
    print("  lengths:", lens)
    if len(lens)==1:
        s = combine(codes_lists)
        print("  base32 out:", s)
        # try decode crockford
        try:
            import base64
            # convert crockford to standard base32
            std = ''.join(c.upper() for c in s)
            # Crockford lacks I,L,O,U; standard mapping
            pad = "="*((8-len(std)%8)%8)
            dec = base64.b32decode((std+pad).encode())
            print("  decoded bytes:", dec)
            print("  as ascii:", dec.decode('latin1'))
        except Exception as e:
            print("  decode err:", e)
