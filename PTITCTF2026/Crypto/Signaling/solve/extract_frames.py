import cv2
import os

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video stream or file")
else:
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    print(f"FPS: {fps}, Total Frames: {total_frames}, Duration: {duration:.2f}s")
    
    # Save a frame every second
    os.makedirs("frames", exist_ok=True)
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % int(fps) == 0:
            cv2.imwrite(f"frames/frame_{count}.jpg", frame)
        count += 1
    
cap.release()
print(f"Extracted {count} frames.")
