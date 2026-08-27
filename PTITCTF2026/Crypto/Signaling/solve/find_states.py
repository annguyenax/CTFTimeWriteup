import cv2
import numpy as np

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error")
    exit()

# Define the 8 sectors by their angle
# The circle is centered in the image. Let's find the center and radius.
# We can just use masks or sample points.
ret, frame = cap.read()
h, w = frame.shape[:2]
cx, cy = w // 2, h // 2

# sample points for the 8 sectors (at some radius)
r = 200 # adjust based on image size, the image is 1080x1440 or something?
print(f"Video resolution: {w}x{h}, center: {cx},{cy}")

# Let's save one frame and find good sample points
cv2.imwrite("sample.jpg", frame)

# We can just track changes in the image.
prev_frame = None
changes = []
count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    # Check if this frame is significantly different from the previous recorded change
    if prev_frame is not None:
        diff = cv2.absdiff(frame, prev_frame)
        if np.mean(diff) > 2.0: # threshold for change
            changes.append(count)
            prev_frame = frame.copy()
    else:
        prev_frame = frame.copy()
        changes.append(count)
        
    count += 1

print(f"Found {len(changes)} distinct states at frames: {changes}")
cap.release()
