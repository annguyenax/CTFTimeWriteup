import cv2
import math
import numpy as np

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    exit()

ret, frame = cap.read()
h, w = frame.shape[:2]
cx, cy = w // 2, h // 2

# We will sample concentric circles to find the hands accurately.
radii = [40, 60, 80, 100, 120]

frames = [38, 48, 58, 68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 178, 188, 198, 208, 218, 228, 238, 248, 258, 268, 278, 288, 298, 308, 318, 328, 338, 348, 358, 368, 378, 388, 398, 408, 418, 428, 438, 448]
# angles for the 8 directions
# 0=N, 1=NE, 2=E, 3=SE, 4=S, 5=SW, 6=W, 7=NW
target_angles = {
    0: 270, 1: 315, 2: 0, 3: 45, 
    4: 90, 5: 135, 6: 180, 7: 225
}

count = 0
results = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    if count in frames:
        scores = {k: 0 for k in range(8)}
        for r in radii:
            for k, a in target_angles.items():
                rad = math.radians(a)
                px = int(cx + r * math.cos(rad))
                py = int(cy + r * math.sin(rad))
                b, g, red = frame[py, px]
                if b > 180 and g > 180 and red > 180:
                    scores[k] += 1
        
        # A hand is present if score is high (e.g., > 2)
        hands = [k for k, v in scores.items() if v >= 2]
        results.append((count, hands))
        
    count += 1

cap.release()
for r in results:
    print(f"Frame {r[0]}: {r[1]}")
