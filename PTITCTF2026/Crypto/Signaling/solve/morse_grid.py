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

morse = {
 '.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F','--.':'G',
 '....':'H','..':'I','.---':'J','-.-':'K','.-..':'L','--':'M','-.':'N',
 '---':'O','.--.':'P','--.-':'Q','.-.':'R','...':'S','-':'T','..-':'U',
 '...-':'V','.--':'W','-..-':'X','-.--':'Y','--..':'Z',
 '-----':'0','.----':'1','..---':'2','...--':'3','....-':'4','.....':'5',
 '-....':'6','--...':'7','---..':'8','----.':'9'
}

for th_off in [np.median(s)+3, np.median(s)+5, np.median(s)+8, 190, 195, 200]:
    bits = (s > th_off).astype(int)
    runs = []; cur = bits[0]; st = 0
    for k in range(1, len(bits)):
        if bits[k] != cur:
            runs.append((st, k-1, cur)); cur = bits[k]; st = k
    runs.append((st, len(bits)-1, cur))
    on_durs = [e-s+1 for (s,e,v) in runs if v == 1]
    off_durs = [e-s+1 for (s,e,v) in runs if v == 0 and s > 0]
    dot_th = int(max(on_durs)*0.6)
    # gap thresholds: try elem/char/word
    for elem_g, char_g, word_g in [(3,6,10),(3,10,16),(3,13,20),(4,10,18),(5,12,20),(6,14,22)]:
        msg = ''; curchar = ''
        i = 0
        while i < len(runs):
            st, en, v = runs[i]
            dur = en - st + 1
            if v == 1:
                curchar += '.' if dur <= dot_th else '-'
            else:
                if i == 0:
                    pass
                elif dur <= elem_g:
                    pass
                elif dur <= char_g:
                    msg += morse.get(curchar, '?'); curchar = ''
                else:
                    msg += morse.get(curchar, '?'); msg += ' '; curchar = ''
            i += 1
        msg += morse.get(curchar, '?')
        if 'PTIT' in msg or 'flag' in msg.lower() or 'ctf' in msg.lower() or msg.count('?') <= 1:
            print('th', round(th_off,1), 'dot<=%d gaps(%d,%d,%d):'%(dot_th,elem_g,char_g,word_g), msg)
