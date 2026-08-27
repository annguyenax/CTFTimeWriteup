import cv2
import math

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    exit()

ret, frame = cap.read()
h, w = frame.shape[:2]
cx, cy = w // 2, h // 2
r_hands = 45 # both hands should be visible here

angles = {0: 270, 1: 315, 2: 0, 3: 45, 4: 90, 5: 135, 6: 180, 7: 225}
frames = [38, 48, 58, 68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 178, 188, 198, 208, 218, 228, 238, 248, 258, 268, 278, 288, 298, 308, 318, 328, 338, 348, 358, 368, 378, 388, 398, 408, 418, 428, 438, 448]

count = 0
out = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    if count in frames:
        vals = []
        for idx, a in angles.items():
            rad = math.radians(a)
            px = int(cx + r_hands * math.cos(rad))
            py = int(cy + r_hands * math.sin(rad))
            vals.append(frame[py, px].mean())
        
        # find the top 2 values
        sorted_vals = sorted(enumerate(vals), key=lambda x: x[1], reverse=True)
        hand1 = sorted_vals[0][0]
        hand2 = sorted_vals[1][0]
        # if the second hand is much dimmer, maybe they overlap
        if sorted_vals[1][1] < 150:
            hand2 = hand1
            
        out.append((count, hand1, hand2))
    count += 1
cap.release()

for o in out:
    print(o)
