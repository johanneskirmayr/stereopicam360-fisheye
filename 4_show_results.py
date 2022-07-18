# Copyright (C) 2021 Eugene a.k.a. Realizator, stereopi.com, virt2real team
#
# This file is part of StereoPi tutorial scripts.
#
# StereoPi tutorial is free software: you can redistribute it 
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the 
# License, or (at your option) any later version.
#
# StereoPi tutorial is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with StereoPi tutorial.  
# If not, see <http://www.gnu.org/licenses/>.
#
#          <><><> SPECIAL THANKS: <><><>
#
# Thanks to Adrian and http://pyimagesearch.com, as a lot of
# code in this tutorial was taken from his lessons.
#  
# Thanks to RPi-tankbot project: https://github.com/Kheiden/RPi-tankbot
#
# Thanks to rakali project: https://github.com/sthysel/rakali


import os
import cv2
import numpy as np

CV_WAITKEY_CURSORKEY_LEFT   = 97
CV_WAITKEY_CURSORKEY_TOP    = 119
CV_WAITKEY_CURSORKEY_RIGHT  = 100 
CV_WAITKEY_CURSORKEY_BOTTOM = 115
CV_WAITKEY_CURSORKEY_PLUS   = 112
CV_WAITKEY_CURSORKEY_MINUS  = 109

fov = 240

# Global variables preset
total_photos = 50

# Camera resolution
photo_width = 480 #1280
photo_height = 480 #480

# Image resolution for processing
img_width =  480# 320
img_height = 480 # 240
image_size = (img_width,img_height)

# Chessboard parameters
rows = 6
columns = 9
square_size = 2.5

# Visualization options
drawCorners = False
showSingleCamUndistortionResults = True
showStereoRectificationResults = True
writeUdistortedImages = True
# imageToDisp = './scenes/scene_1280x480_1.png'
imageToDisp = './calib_files/stereo_30.png'

if (drawCorners):
    print("You can press 'Q' to quit this script.")

center_x, center_y = img_width/2, img_height/2

"""
# Takes an image in as a numpy array and undistorts it
"""

print("Undistorting picture with (width, height):", (img_width, img_height))
try:
    npz_file = np.load('./calibration_data/{}p/camera_calibration{}.npz'.format(h, '_left'))
    if 'map1' and 'map2' in npz_file.files:
        #print("Camera calibration data has been found in cache.")
        map1 = npz_file['map1']
        map2 = npz_file['map2']
    else:
        print("Camera data file found but data corrupted.")
        exit(0)
except:
    print("Camera calibration data not found in cache, file " & './calibration_data/{}p/camera_calibration{}.npz'.format(h, left))
    exit(0)

# We didn't load a new image from file, but use last image loaded while calibration
cap_0 = cv2.VideoCapture(0)
cap_1 = cv2.VideoCapture(1)


while(True):

    ret, frame_left = cap_0.read()
    ret, frame_right = cap_1.read()

    #frame_left = frame_left[100:380,180:460]
    #frame_right = frame_right[100:380,180:460]
    frame_left = frame_left[:,80:560]
    frame_right = frame_right[:,80:560]

    undistorted_left = cv2.remap(frame_left, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    #h, w = imgR.shape[:2]
    print("Undistorting picture with (width, height):", (w, h))
    try:
        npz_file = np.load('./calibration_data/{}p/camera_calibration{}.npz'.format(h, '_right'))
        if 'map1' and 'map2' in npz_file.files:
            #print("Camera calibration data has been found in cache.")
            map1 = npz_file['map1']
            map2 = npz_file['map2']
        else:
            print("Camera data file found but data corrupted.")
            exit(0)
    except:
        print("Camera calibration RIGHT data not found in cache.")
        exit(0)

    undistorted_right = cv2.remap(frame_right, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    w, h = fov, fov
    x = center_x - w/2
    y = center_y - h/2
    frame_cropped_left = undistorted_left[int(y):int(y+h), int(x):int(x+w)]
    frame_cropped_right = undistorted_right[int(y):int(y+h), int(x):int(x+w)]

    cv2.imshow('PiCam left', frame_cropped_left)
    cv2.imshow('PiCam right', frame_cropped_right)
    cv2.imshow('PiCam all left', undistorted_left)
    cv2.imshow('PiCam all right', undistorted_right)
    # cv2.imshow('____', _)
    
    key = cv2.waitKey(100)
    if key == ord('q'):
        break
    elif key == CV_WAITKEY_CURSORKEY_TOP:
        center_y += 10
    elif key == CV_WAITKEY_CURSORKEY_BOTTOM:
        center_y -= 10
    elif key == CV_WAITKEY_CURSORKEY_LEFT:
        center_x -= 10
    elif key == CV_WAITKEY_CURSORKEY_RIGHT:
        center_x += 10
    elif key == CV_WAITKEY_CURSORKEY_MINUS:
        fov += 20
    elif key == CV_WAITKEY_CURSORKEY_PLUS:
        fov -= 20
    elif key == -1:
        pass
    else:
        print("key=%d" % key)

cv2.destroyAllWindows()

if (writeUdistortedImages):
    cv2.imwrite("undistorted_left.jpg",undistorted_left)
    cv2.imwrite("undistorted_right.jpg",undistorted_right)