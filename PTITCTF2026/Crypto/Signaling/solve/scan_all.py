import cv2
import math

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

r_sec = 250
r_hands = 70
sec_angles = {0: 270, 1: 315, 2: 0, 3: 45, 4: 90, 5: 135, 6: 180, 7: 225}
angle_to_idx = {270:0, 315:1, 0:2, 45:3, 90:4, 135:5, 180:6, 225:7}

out = []
last_state = []
count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    
    # Sectors
    state = []
    for idx, a in sec_angles.items():
        rad = math.radians(a)
        px = int(cx + r_sec * math.cos(rad))
        py = int(cy + r_sec * math.sin(rad))
        patch = frame[py-5:py+5, px-5:px+5]
        if patch.mean() > 150:
            state.append(idx)
            
    if len(state) == 2 and state != last_state:
        # We found a new valid sector state! Now read hands!
        angles_found = []
        for angle in range(360):
            rad = math.radians(angle)
            px = int(cx + r_hands * math.cos(rad))
            py = int(cy + r_hands * math.sin(rad))
            b,g,r = frame[py, px]
            if b > 200 and g > 200 and r > 200:
                angles_found.append(angle)
        
        clusters = []
        if angles_found:
            curr = [angles_found[0]]
            for i in range(1, len(angles_found)):
                if angles_found[i] - angles_found[i-1] <= 3:
                    curr.append(angles_found[i])
                else:
                    clusters.append(curr)
                    curr = [angles_found[i]]
            if len(clusters) > 0 and 359 in curr and 0 in clusters[0]:
                clusters[0].extend(curr)
            else:
                clusters.append(curr)
        
        hand_idx = []
        for c in clusters:
            avg_angle = sum(c) / len(c)
            nearest = round(avg_angle / 45) * 45
            if nearest == 360: nearest = 0
            hand_idx.append(angle_to_idx[nearest])
            
        out.append((count, state, list(set(hand_idx))))
        last_state = state
    elif len(state) == 0:
        last_state = []
        
    count += 1

cap.release()

for item in out:
    print(item)
