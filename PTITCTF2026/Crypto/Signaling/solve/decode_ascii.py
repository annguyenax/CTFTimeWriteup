import cv2
import math

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    exit()

ret, frame = cap.read()
h, w = frame.shape[:2]
cx, cy = w // 2, h // 2
r = 300

angles = {
    'N': 270, 'NE': 315, 'E': 0, 'SE': 45,
    'S': 90, 'SW': 135, 'W': 180, 'NW': 225
}
sector_names = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

last_state = None
states = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    state = []
    for name in sector_names:
        angle = angles[name]
        rad = math.radians(angle)
        px = int(cx + r * math.cos(rad))
        py = int(cy + r * math.sin(rad))
        patch = frame[py-5:py+5, px-5:px+5]
        state.append(patch.mean())
    
    binary_state = [1 if v > 150 else 0 for v in state]
    if sum(binary_state) > 0 and binary_state != last_state:
        states.append(binary_state)
        last_state = binary_state
    elif sum(binary_state) == 0 and last_state is not None:
        last_state = None

cap.release()

# Now we have a list of states.
# Try mapping each 8-bit array to ASCII character in all 8 rotations
# both forwards and backwards
for rot in range(8):
    for reverse in [False, True]:
        result = ""
        for s in states:
            shifted = s[rot:] + s[:rot]
            if reverse:
                shifted = shifted[::-1]
            val = sum(v * (1 << (7 - i)) for i, v in enumerate(shifted))
            result += chr(val) if 32 <= val <= 126 else "."
        if "PTIT" in result or "ptit" in result:
            print(f"Rot: {rot}, Rev: {reverse}, Output: {result}")
