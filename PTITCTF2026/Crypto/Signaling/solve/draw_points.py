import cv2
import math

frame = cv2.imread(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\frames\frame_50.jpg")
h, w = frame.shape[:2]
cx, cy = w // 2, h // 2
r = 250 # guess

angles = {
    'N': 270, 'NE': 315, 'E': 0, 'SE': 45,
    'S': 90, 'SW': 135, 'W': 180, 'NW': 225
}

for name, angle in angles.items():
    rad = math.radians(angle)
    px = int(cx + r * math.cos(rad))
    py = int(cy + r * math.sin(rad))
    cv2.circle(frame, (px, py), 10, (0, 0, 255), -1)
    cv2.putText(frame, name, (px+15, py), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

cv2.imwrite("points.jpg", frame)
