import random, math, string, re

ct = "KGBTKEBSJVVCODVKERUDKHPWCFJJTLNPEOFVJBXJIHMKCLJTCGMBUPXTVCADJBLGQJIMNQJZFW"

# n-gram frequencies from standard english (simplified)
ngrams = {}
# let's just use a basic trigram list
trigrams = "THE AND THA ENT ION TIO FOR NDE HAS NCE EDT TIS OFT STH MEN"
for t in trigrams.split():
    ngrams[t] = 100

def score(text):
    s = 0
    for i in range(len(text)-2):
        tri = text[i:i+3]
        if tri in ngrams:
            s += ngrams[tri]
    return s

# actually hill climbing requires a good quadgram file.
# Let's just print it and I will guess some letters.
# J=E, K=T, B=H?
# If K=T, B=H, J=E:
# T G H T T   E H S E V V C O D V T E R U D T H P W C F E E T L N P E O F V E H X E I H M T C L E T C G M H U P X T V C A D E H L G Q E I M N Q E Z F W
