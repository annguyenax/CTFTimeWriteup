import cv2, numpy as np

c = cv2.VideoCapture(r'files\extracted\Signaling\Signaling.mp4')
sig = []
while True:
    ok, fr = c.read()
    if not ok:
        break
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    sig.append(float(g[150:400, 350:750].max()))
s = np.array(sig)
th = np.median(s) + 5
bits = (s > th).astype(int)

runs = []
cur = bits[0]; st = 0
for k in range(1, len(bits)):
    if bits[k] != cur:
        runs.append((st, k - 1, cur)); cur = bits[k]; st = k
runs.append((st, len(bits) - 1, cur))

morse = {
 '.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G',
 '....':'H','..':'I','.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N',
 '---':'O','.--.':'P','--.-':'Q','.-.':'R','...':'S','-':'T','..-':'U',
 '...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z',
 '-----':'0','.----':'1','..---':'2','...--':'3','....-':'4','.....':'5',
 '-....':'6','--...':'7','---..':'8','----.':'9',
 '.-.-.-':'.','--..--':',','..--..':'?','-.-.--':'!'
}

msg = ''
curchar = ''
i = 0
while i < len(runs):
    st, en, v = runs[i]
    dur = en - st + 1
    if v == 1:
        curchar += '.' if dur <= 10 else '-'
    else:
        if i == 0:
            pass
        elif dur <= 6:
            pass  # element gap
        elif dur <= 20:
            msg += morse.get(curchar, '?'); curchar = ''
        else:
            msg += morse.get(curchar, '?'); msg += ' '; curchar = ''
    i += 1
msg += morse.get(curchar, '?')
print('DECODED:', msg)
