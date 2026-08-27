import cv2
import math

frame = cv2.imread(r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\solve\hand_48.jpg')
h, w = frame.shape[:2]
cx, cy = w//2, h//2
for a in range(0, 360, 45):
    rad = math.radians(a)
    px = int(cx + 100 * math.cos(rad))
    py = int(cy + 100 * math.sin(rad))
    cv2.line(frame, (cx, cy), (px, py), (0,0,255), 2)
    cv2.putText(frame, str(a), (px, py), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

cv2.imwrite('D:\\download\\CTFTimeWriteup\\PTITCTF2026\\Crypto\\Signaling\\solve\\hand_48_annotated.jpg', frame)
