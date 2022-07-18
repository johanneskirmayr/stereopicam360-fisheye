import cv2
import numpy as np
import time

cap_0 = cv2.VideoCapture(2)
cap_1 = cv2.VideoCapture(3)

for i in range(50):
    ret, frame_left = cap_0.read()
    time.sleep(2)
    ret, frame_right = cap_1.read()
    
    cv2.imwrite(f"calib_files/left_{str(i).zfill(2)}.png", frame_left)
    cv2.imwrite(f"calib_files/right{str(i).zfill(2)}.png", frame_right)
    
    #cv2.imshow('frame',frame_left)

    time.sleep(2)

cap_0.release()
cap_1.release()

cv2.destroyAllWindows()


