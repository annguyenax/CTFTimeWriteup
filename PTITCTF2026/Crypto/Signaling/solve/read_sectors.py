import cv2
import math

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error")
    exit()

ret, frame = cap.read()
h, w = frame.shape[:2]
cx, cy = w // 2, h // 2
r = 300 # radius to sample (adjusting a bit)

angles = {
    'N': 270, 'NE': 315, 'E': 0, 'SE': 45,
    'S': 90, 'SW': 135, 'W': 180, 'NW': 225
}
# Order for 8-bit mapping: N, NE, E, SE, S, SW, W, NW
# Let's see what happens.
sector_names = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

count = 0
active_states = []
last_state = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    # Sample intensity at each sector
    state = []
    for name in sector_names:
        angle = angles[name]
        rad = math.radians(angle)
        px = int(cx + r * math.cos(rad))
        py = int(cy + r * math.sin(rad))
        
        # Get a small patch mean
        patch = frame[py-5:py+5, px-5:px+5]
        intensity = patch.mean()
        # High intensity = highlighted. The dark blue background is around 100-150?
        # The highlighted light blue is much brighter.
        state.append(intensity)
    
    # Thresholding to binary (1 if highlighted, 0 otherwise)
    # We can use a threshold. Let's say if intensity > 180 it's highlighted.
    # Alternatively, we can just find the max intensities.
    # Since we expect 2 highlighted sectors (semaphore), or some specific number.
    binary_state = [1 if v > 150 else 0 for v in state] # adjust threshold if needed
    
    if sum(binary_state) > 0 and binary_state != last_state:
        # Avoid duplicate consecutive prints
        print(f"Frame {count}: {binary_state}, values: {[int(v) for v in state]}")
        last_state = binary_state
    elif sum(binary_state) == 0 and last_state is not None:
        last_state = None # reset when it goes blank
        
    count += 1
