import cv2

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

frames = [38, 48, 58, 68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 178, 188]
count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    if count in frames:
        cv2.imwrite(f"D:\\download\\CTFTimeWriteup\\PTITCTF2026\\Crypto\\Signaling\\solve\\hand_{count}.jpg", frame)
    count += 1
cap.release()
