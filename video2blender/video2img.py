import cv2 as cv
import os

video_path = './video/video.mp4'
dir_path = './image'
basename = 'img_frame'
ext = 'jpg'

cap = cv.VideoCapture(video_path)
if not cap.isOpened():
    exit()

os.makedirs(dir_path, exist_ok=True)
base_path = os.path.join(dir_path, basename)
digit = len(str(int(cap.get(cv.CAP_PROP_FRAME_COUNT))))

n = 0
while True:
    ret, frame = cap.read()
    if ret:
        cv.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
        n += 1
    else:
        exit()
