import cv2
import math

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    exit()

ret, frame = cap.read()
h, w = frame.shape[:2]
cx, cy = w // 2, h // 2
r = 250 # radius to sample inside the sector

# Sector centers in degrees (0 is East/Right, increasing clockwise)
# 12:00 is -90 or 270.
# The boundaries are at 270, 315, 0, 45, 90, 135, 180, 225.
# The centers of the sectors are at:
# 292.5 (10:30 to 12:00 -> top left?) Wait.
# Boundaries at 12 (270), 1:30 (315), 3 (0), 4:30 (45), 6 (90), 7:30 (135), 9 (180), 10:30 (225)
# Sector centers:
# 12 to 1:30 -> 292.5
# 1:30 to 3 -> 337.5
# 3 to 4:30 -> 22.5
# 4:30 to 6 -> 67.5
# 6 to 7:30 -> 112.5
# 7:30 to 9 -> 157.5
# 9 to 10:30 -> 202.5
# 10:30 to 12 -> 247.5

angles = [292.5, 337.5, 22.5, 67.5, 112.5, 157.5, 202.5, 247.5]
sector_names = ['12-1:30', '1:30-3', '3-4:30', '4:30-6', '6-7:30', '7:30-9', '9-10:30', '10:30-12']

last_state = None
count = 0
states = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    state = []
    for angle in angles:
        rad = math.radians(angle)
        px = int(cx + r * math.cos(rad))
        py = int(cy + r * math.sin(rad))
        patch = frame[py-5:py+5, px-5:px+5]
        state.append(patch.mean())
    
    binary_state = [1 if v > 150 else 0 for v in state]
    if sum(binary_state) > 0 and binary_state != last_state:
        print(f"Frame {count}: {binary_state}")
        states.append(binary_state)
        last_state = binary_state
    elif sum(binary_state) == 0 and last_state is not None:
        last_state = None
        
    count += 1

cap.release()
