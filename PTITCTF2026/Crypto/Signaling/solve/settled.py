import cv2
import math

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

r_sec = 250
r_hands = 70
sec_angles = {0: 270, 1: 315, 2: 0, 3: 45, 4: 90, 5: 135, 6: 180, 7: 225}

frames = [39, 49, 59, 69, 79, 89, 99, 109, 119, 129, 139, 149, 159, 169, 179, 189, 199, 209, 219, 229, 239, 249, 259, 269, 279, 289, 299, 309, 319, 329, 339, 349, 359, 369, 379, 389, 399, 409, 419, 429, 439, 449]

out = []
for count in frames:
    cap.set(cv2.CAP_PROP_POS_FRAMES, count)
    ret, frame = cap.read()
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    state = []
    for idx, a in sec_angles.items():
        rad = math.radians(a)
        px = int(cx + r_sec * math.cos(rad))
        py = int(cy + r_sec * math.sin(rad))
        patch = frame[py-5:py+5, px-5:px+5]
        if patch.mean() > 150:
            state.append(idx)
            
    cap.set(cv2.CAP_PROP_POS_FRAMES, count + 4) # hands settle!
    ret, frame = cap.read()
    hand_idx = []
    for idx, a in sec_angles.items():
        rad = math.radians(a)
        px = int(cx + r_hands * math.cos(rad))
        py = int(cy + r_hands * math.sin(rad))
        b,g,r = frame[py, px]
        if b > 200 and g > 200 and r > 200:
            hand_idx.append(idx)
        
    out.append((count, state, hand_idx))

cap.release()

sema = {
    (0,1):'A', (0,2):'B', (0,3):'C', (0,4):'D', (0,5):'E', (0,6):'F', (0,7):'G',
    (1,2):'H', (1,3):'I', (4,6):'J', (1,4):'K', (1,5):'L', (1,6):'M', (1,7):'N',
    (2,3):'O', (2,4):'P', (2,5):'Q', (2,6):'R', (2,7):'S', (3,4):'T', (3,5):'U',
    (4,7):'V', (5,6):'W', (5,7):'X', (3,6):'Y', (6,7):'Z', (3,7):' '
}

res_sec = ''
res_hand = ''
for c, s, h in out:
    if len(s) == 2:
        s1, s2 = min(s), max(s)
        res_sec += sema.get((s1, s2), '?')
    else: res_sec += '?'
    
    if len(h) == 2:
        h1, h2 = min(h), max(h)
        res_hand += sema.get((h1, h2), '?')
    elif len(h) == 1:
        res_hand += sema.get((h[0], h[0]), '?') # Or whatever
    else: res_hand += '?'

print('Sectors:', res_sec)
print('Hands:', res_hand)
