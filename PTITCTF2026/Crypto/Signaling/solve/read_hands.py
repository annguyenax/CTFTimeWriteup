import cv2
import numpy as np
import math

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    exit()

ret, frame = cap.read()
h, w = frame.shape[:2]
cx, cy = w // 2, h // 2
r_hands = 70 # radius to check hands

# Frames where we detected a state change
frames = [38, 48, 58, 68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 178, 188, 198, 208, 218, 228, 238, 248, 258, 268, 278, 288, 298, 308, 318, 328, 338, 348, 358, 368, 378, 388, 398, 408, 418, 428, 438, 448]

count = 0
hand_angles = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    if count in frames:
        # Check 360 degrees to find the hands
        angles_found = []
        for angle in range(360):
            rad = math.radians(angle)
            px = int(cx + r_hands * math.cos(rad))
            py = int(cy + r_hands * math.sin(rad))
            # The hands are white, so B,G,R should be high
            b,g,r = frame[py, px]
            if b > 200 and g > 200 and r > 200:
                angles_found.append(angle)
        
        # Group adjacent angles
        clusters = []
        if angles_found:
            curr_cluster = [angles_found[0]]
            for i in range(1, len(angles_found)):
                if angles_found[i] - angles_found[i-1] <= 3:
                    curr_cluster.append(angles_found[i])
                else:
                    clusters.append(curr_cluster)
                    curr_cluster = [angles_found[i]]
            # wrap around 360 to 0
            if len(clusters) > 0 and 359 in curr_cluster and 0 in clusters[0]:
                clusters[0].extend(curr_cluster)
            else:
                clusters.append(curr_cluster)
        
        hand_dirs = []
        for c in clusters:
            avg_angle = sum(c) / len(c)
            # map to nearest 45 degree (0, 45, 90, 135, 180, 225, 270, 315)
            nearest = round(avg_angle / 45) * 45
            if nearest == 360: nearest = 0
            hand_dirs.append(nearest)
            
        print(f"Frame {count}: Hand angles = {list(set(hand_dirs))}")
        
    count += 1

cap.release()
