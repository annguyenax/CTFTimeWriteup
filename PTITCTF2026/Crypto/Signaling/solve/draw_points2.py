import cv2
import math

frame = cv2.imread(r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\frames\frame_50.jpg")
h, w = frame.shape[:2]
cx, cy = w // 2, h // 2
r = 250 

angles = [292.5, 337.5, 22.5, 67.5, 112.5, 157.5, 202.5, 247.5]
for i, angle in enumerate(angles):
    rad = math.radians(angle)
    px = int(cx + r * math.cos(rad))
    py = int(cy + r * math.sin(rad))
    cv2.circle(frame, (px, py), 10, (0, 0, 255), -1)
    cv2.putText(frame, str(i), (px+15, py), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

cv2.imwrite("points2.jpg", frame)
