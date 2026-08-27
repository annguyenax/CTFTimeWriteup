import cv2

video_path = r"D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\Signaling\files\extracted\Signaling\Signaling.mp4"
cap = cv2.VideoCapture(video_path)

frames_to_save = [68, 178, 298]
count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    if count in frames_to_save:
        cv2.imwrite(f"D:\\download\\CTFTimeWriteup\\PTITCTF2026\\Crypto\\Signaling\\solve\\frame_{count}.jpg", frame)
    count += 1
cap.release()
