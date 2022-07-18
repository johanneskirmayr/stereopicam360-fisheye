import cv2
import numpy as np
import time

cap_0 = cv2.VideoCapture(0)
cap_1 = cv2.VideoCapture(1)

for i in range(50):
    ret, frame_left = cap_0.read()
    ret, frame_right = cap_1.read()

    #frame_left = frame_left[100:380,180:460]
    #frame_right = frame_right[100:380,180:460]
    frame_left = frame_left[:,80:560]
    frame_right = frame_right[:,80:560]

    print(frame_left.shape)
    
    cv2.imwrite(f"calib_files/left_{str(i).zfill(2)}.png", frame_left)
    cv2.imwrite(f"calib_files/right_{str(i).zfill(2)}.png", frame_right)
    
    cv2.imshow('frame left',frame_left)
    cv2.imshow('frame right',frame_right)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break

    time.sleep(1)
    if i == 30:
        stereo_frame=np.concatenate((frame_left,frame_right),1)
        cv2.imwrite(f"calib_files/stereo_{str(i).zfill(2)}.png", stereo_frame)

cap_0.release()
cap_1.release()

cv2.destroyAllWindows()


