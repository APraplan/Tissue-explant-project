import cv2
import numpy as np
import sys
sys.path.append('c:/Users/APrap/Documents/CREATE/Pick-and-Place/Platform')

import computer_vision as mcv
import pickle

detect_chessboard = False
detect_sample = True

num = 0

cap = cv2.VideoCapture(0) 

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")
    
mcv.make_720p(cap)
    
ret, frame = cap.read() 

cam = mcv.Camera(frame)
frame = cam.undistort(frame)

mask = np.zeros(frame.shape[0:2], dtype='uint8')
center_coordinates = (int(mask.shape[1]/2), int(mask.shape[0]/2))
radius = 170
color = 255
thickness = -1
mask = cv2.circle(mask, center_coordinates, radius, color, thickness)

chessboardSize = (9, 6)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

printed = False
    
while(True): 

    # reads frames from a camera 
    _, frame = cap.read() 
    frame = cam.undistort(frame)
    
    cv2.imshow('Camera', frame) 
       
    # Detection
    if detect_sample:
        out = mcv.detection_test(frame, mask)
        cv2.imshow('Detection', out)
    
    # # Detection chessboard
    if detect_chessboard:
        out = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)
        if ret:
            corners = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            out = cv2.drawChessboardCorners(out, chessboardSize, corners, ret)
        cv2.imshow('Chessboard', out)
    
    if not printed:
        print(out.shape)
        printed = True
        
    cv2.imshow('Calibrated camera', out) 

    # Wait for Esc key to stop 
    k = cv2.waitKey(5) & 0xFF
    if k == ord('p'):
        # path = "C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\image" + str(num)
        cv2.imwrite("Pictures\Realsample\image" + str(num) + ".png", frame)
        num += 1
        pass
    
    if k == 27: 
        break
    
cap.release() 
cv2.destroyAllWindows()


