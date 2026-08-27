import cv2
import math

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    exit()

ret, frame = cap.read()
h, w = frame.shape[:2]
cx, cy = w // 2, h // 2

# The 8 tick marks are at:
# 12:00 = 270
# 1:30 = 315
# 3:00 = 0
# 4:30 = 45
# 6:00 = 90
# 7:30 = 135
# 9:00 = 180
# 10:30 = 225

angles = {
    0: 270, 1: 315, 2: 0, 3: 45,
    4: 90, 5: 135, 6: 180, 7: 225
}

frames = [38, 48, 58, 68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 178, 188, 198, 208, 218, 228, 238, 248, 258, 268, 278, 288, 298, 308, 318, 328, 338, 348, 358, 368, 378, 388, 398, 408, 418, 428, 438, 448]

# To distinguish hour (short) and minute (long) hands, we sample at two radii:
r_short = 50
r_long = 120

count = 0
results = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    if count in frames:
        hour_idx = -1
        minute_idx = -1
        
        # Find minute hand (long)
        best_val = 0
        for idx, a in angles.items():
            rad = math.radians(a)
            px = int(cx + r_long * math.cos(rad))
            py = int(cy + r_long * math.sin(rad))
            val = frame[py, px].mean()
            if val > best_val:
                best_val = val
                minute_idx = idx
                
        # Find hour hand (short)
        # It could be at the same position as the minute hand.
        best_val = 0
        for idx, a in angles.items():
            rad = math.radians(a)
            px = int(cx + r_short * math.cos(rad))
            py = int(cy + r_short * math.sin(rad))
            val = frame[py, px].mean()
            # If it's the minute hand's direction, it will also be bright here.
            # But the hour hand is thicker or we can just pick the top 2 if they are different.
            if val > best_val and idx != minute_idx:
                best_val = val
                hour_idx = idx
                
        # If best_val for hour hand is low, it means both hands are in the same direction!
        if best_val < 150:
            hour_idx = minute_idx
            
        results.append((count, hour_idx, minute_idx))
    count += 1
cap.release()

for r in results:
    print(r)
