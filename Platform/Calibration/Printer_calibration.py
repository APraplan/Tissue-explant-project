import cv2
import numpy as np
import pickle
import glob
import sys
sys.path.append('c:/Users/APrap/Documents/CREATE/Pick-and-Place/Platform')
import computer_vision as mcv
from Communication.printer_communications import *

chessboardSize = (9, 6)
size_of_chessboard_squares_mm = 10
calibration_position = (100, 180)

cam_number = 0
printer_port = 'COM15'

chessboard_calibration = False
test_chessboard_calibration = False
bed_leveling_calibration = False
verticality_calibration = True
offset_callibration = True
camera_calibration = True
test_camera_calibration = True


cap = cv2.VideoCapture(cam_number) 

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")
    
mcv.make_720p(cap)
    
ret, frame = cap.read() 


if chessboard_calibration:
    
    num = 0
            
    while(True): 

        # reads frames from a camera 
        _, frame = cap.read() 
                    
        cv2.imshow('Push "p" to take calibration pictures', frame) 
                
        key = cv2.waitKey(5) & 0xFF
        if key == ord('p'):
            # path = "C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\image" + str(num)
            cv2.imwrite("Pictures\calibration\image" + str(num) + ".png", frame)
            num += 1
            pass
        
        if key == 27: 
            cv2.destroyAllWindows()
            break
        
    frameSize = (frame.shape[1], frame.shape[0])

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

    objp = objp * size_of_chessboard_squares_mm


    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.


    images = glob.glob('Pictures\calibration\*.png')


    for image in images:

        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

        # If found, add object points, image points (after refining them)
        if ret == True:

            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)

            # Draw and display the corners
            cv2.drawChessboardCorners(img, chessboardSize, corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(5)


    cv2.destroyAllWindows()


    ############## CALIBRATION #######################################################

    ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

    pickle.dump((cameraMatrix, dist), open('Platform/Calibration/calibration.pkl', 'wb'))
    pickle.dump(cameraMatrix, open('Platform/Calibration/cameraMatrix.pkl', 'wb'))
    pickle.dump(dist, open('Platform/Calibration/dist.pkl', 'wb'))


    # Reprojection Error
    mean_error = 0

    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error

    print( "total error: {}".format(mean_error/len(objpoints)) )
    
cam = mcv.Camera(frame)
    
if test_chessboard_calibration:
        
    while(True): 

        # reads frames from a camera 
        _, frame = cap.read() 
        imshow = cam.undistort(frame)
            
        cv2.imshow('Camera', frame) 
        cv2.imshow('Udistort', imshow) 
        
        key = cv2.waitKey(5) & 0xFF
        
        if key == 27: 
            cv2.destroyAllWindows()
            break

if verticality_calibration or offset_callibration or camera_calibration or test_camera_calibration or bed_leveling_calibration:
    
    anycubic = Printer(descriptive_device_name="printer", port_name=printer_port, baudrate=115200)
    
    anycubic.connect()
    anycubic.homing()
    anycubic.max_z_feedrate(20)

if bed_leveling_calibration:
    
    anycubic.move_axis(x=25, y=195, z=0, f = 8000)
    
    while(True): 

        # reads frames from a camera 
        _, frame = cap.read() 
        imshow = cam.undistort(frame)
        
        markerSize = 15
        thickness = 1
        center = (imshow.shape[1]//2, imshow.shape[0]//2)
        imshow = cv2.drawMarker(imshow, center, (255, 0, 0), cv2.MARKER_CROSS, markerSize, thickness)
            
        cv2.imshow('Press "0,1,2,3" to circle', imshow) 
        
        key = cv2.waitKey(5) & 0xFF
        
        if key == ord('0'):
            anycubic.move_axis(z=5, f = 8000)
            anycubic.move_axis(x=25, y=200, f = 8000)
            anycubic.move_axis(z=0, f = 8000)
        if key == ord('1'):
            anycubic.move_axis(z=5, f = 8000)
            anycubic.move_axis(x=175, y=200, f = 8000)
            anycubic.move_axis(z=0, f = 8000)        
        if key == ord('2'):
            anycubic.move_axis(z=5, f = 8000)
            anycubic.move_axis(x=175, y=75, f = 8000)
            anycubic.move_axis(z=0, f = 8000)        
        if key == ord('3'):
            anycubic.move_axis(z=5, f = 8000)
            anycubic.move_axis(x=25, y=75, f = 8000)
            anycubic.move_axis(z=0, f = 8000)        
        if key == 27: 
            cv2.destroyAllWindows()
            break

if verticality_calibration:

    anycubic.move_axis(x=calibration_position[0], y=calibration_position[1], z=5, f = 8000)
    
    while(True): 

        # reads frames from a camera 
        _, frame = cap.read() 
        imshow = cam.undistort(frame)
        
        markerSize = 15
        thickness = 1
        center = (imshow.shape[1]//2, imshow.shape[0]//2)
        imshow = cv2.drawMarker(imshow, center, (255, 0, 0), cv2.MARKER_CROSS, markerSize, thickness)
            
        cv2.imshow('Press "0" to go down and "1" to go up', imshow) 
        
        key = cv2.waitKey(5) & 0xFF
        
        if key == ord('0'):
            anycubic.move_axis(x=calibration_position[0], y=calibration_position[1], z=5, f = 8000)
        if key == ord('1'):
            anycubic.move_axis(x=calibration_position[0], y=calibration_position[1], z=105, f = 8000)
        
        if key == 27: 
            cv2.destroyAllWindows()
            break
        
if offset_callibration:


    anycubic.move_axis(x=calibration_position[0], y=calibration_position[1], z=75, f = 8000)
    
    offset = [-23,-14.4]
    
    while(True): 

        # reads frames from a camera 
        _, frame = cap.read() 
        imshow = cam.undistort(frame)
        
        markerSize = 15
        thickness = 1
        center = (imshow.shape[1]//2, imshow.shape[0]//2)
        imshow = cv2.drawMarker(imshow, center, (255, 0, 0), cv2.MARKER_CROSS, markerSize, thickness)
            
        cv2.imshow('Press "0" to go down and "1" to go up, "w,a,s,d to correct the offset', imshow) 
        
        key = cv2.waitKey(5) & 0xFF
        
        if key == ord('a'):
            offset[0] -= 0.1
            anycubic.move_axis(x=calibration_position[0]+offset[0], y=calibration_position[1]+offset[1], z=2, f = 8000)
            
        if key == ord('d'):
            offset[0] += 0.1
            anycubic.move_axis(x=calibration_position[0]+offset[0], y=calibration_position[1]+offset[1], z=2, f = 8000)
            
        if key == ord('w'):
            offset[1] -= 0.1
            anycubic.move_axis(x=calibration_position[0]+offset[0], y=calibration_position[1]+offset[1], z=2, f = 8000)
            
        if key == ord('s'):
            offset[1] += 0.1
            anycubic.move_axis(x=calibration_position[0]+offset[0], y=calibration_position[1]+offset[1], z=2, f = 8000)
        
        if key == ord('0'):
            anycubic.move_axis(x=calibration_position[0]+offset[0], y=calibration_position[1]+offset[1], z=2, f = 8000)
        if key == ord('1'):
            anycubic.move_axis(x=calibration_position[0], y=calibration_position[1], z=75, f = 8000)
        
        if key == 27: 
            print('Offset = ', offset)
            pickle.dump(offset, open('Platform/Calibration/offset.pkl', 'wb'))
            cv2.destroyAllWindows()
            break
    
if camera_calibration:
     
    z1 = 175
    z2 = 75
    h = 388 # Real perimeter
    
    anycubic.move_axis(x=100, y=100, z=z1, f = 2000)
    pos = z1
    
    while True:
        
        # reads frames from a camera 
        _, frame = cap.read() 
        imshow = cam.undistort(frame)
        
        markerSize = 15
        thickness = 1
        center = (imshow.shape[1]//2, imshow.shape[0]//2)
        imshow = cv2.drawMarker(imshow, center, (255, 0, 0), cv2.MARKER_CROSS, markerSize, thickness)
            
        cv2.imshow('Press "0" to go down and "1" to go up, "p" to save picture', imshow)
        
        key = cv2.waitKey(5) & 0xFF 
        
        if key == ord('0'):
            anycubic.move_axis(x=100, y=100, z=z2, f = 2000)
            pos = z2
        if key == ord('1'): 
            anycubic.move_axis(x=100, y=100, z=z1, f = 2000)
            pos = z1
        if key == ord('p'):
            if pos == z1:
                cv2.imwrite("Pictures\Size\img_z1.png", imshow)
            else:
                cv2.imwrite("Pictures\Size\img_z2.png", imshow)
                        
        if key == 27: 
            cv2.destroyAllWindows()
            break
        
    # Calibration
    
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters =  cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)    
    
    img_z1 = cv2.imread("Pictures\Size\img_z1.png")
    img_z2 = cv2.imread("Pictures\Size\img_z2.png")
    
    markerCorners_z1, _, _ = detector.detectMarkers(img_z1)
    markerCorners_z2, _, _ = detector.detectMarkers(img_z2)

    markerCorners_z1 = np.array(markerCorners_z1[0][0])
    markerCorners_z2 = np.array(markerCorners_z2[0][0])

    a = cv2.arcLength(markerCorners_z1, True)
    b = cv2.arcLength(markerCorners_z2, True)
    
    # z + z_offset = d
    # a/f = h/d
    # b/f = h/(d-m)
    
    m = z1 - z2
    d = m/(1-a/b)
    f = d*a/h
    z_offset = d - z1
    # h = a*d/f = a(z/f + z_offset/f)
    f = [f, f]  
    
    # Tuning
    
    anycubic.move_axis(x=100, y=100, z=100, f = 8000)
    offset = pickle.load(open('Platform/Calibration/offset.pkl', 'rb'))
    
    while True:
        
        # reads frames from a camera 
        _, frame = cap.read() 
        imshow = cam.undistort(frame)
        
        markerCorners, _, _ = detector.detectMarkers(imshow)
        try:
            markerCorners = np.array(markerCorners[0][0])
            int_corners = np.int32(markerCorners)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 2
            color = (255,0, 0)
            thickness = 4

            imshow = cv2.polylines(imshow,  [int_corners], True, (0, 255, 0), 2)
            for i in range(len(int_corners)):
                imshow = cv2.putText(imshow, str(i+1), int_corners[i], font, 
                            fontScale, color, thickness, cv2.LINE_AA)
        except:
            pass
        
        cv2.imshow('Press "enter" to point the aruco marker, "w,a,s,d" to tune the parameters', imshow) 
        
        key = cv2.waitKey(5) & 0xFF 

        if key == ord('a'):
            f[1] += 0.005
            print('f ', f)
            
        if key == ord('d'):
            f[1] -= 0.005
            print('f ', f)
            
        if key == ord('w'):
            f[0] += 0.005
            print('f ', f)
            
        if key == ord('s'):
            f[0] -= 0.005
            print('f ', f)
            
        if key == ord('0'):
            anycubic.move_axis(x=100, y=100, z=75, f = 2000)

        if key == ord('1'): 
            anycubic.move_axis(x=100, y=100, z=100, f = 2000)
            
        if key == ord('2'): 
            anycubic.move_axis(x=100, y=100, z=125, f = 2000)
        
        if key == 13:
            
            pos = anycubic.read_position()
            
            z = pos[2]
            
            coef_x = (z + z_offset)/f[1]
            coef_y = (z + z_offset)/f[0]
            
            center = (imshow.shape[1]//2, imshow.shape[0]//2)
            
            anycubic.move_axis(x=pos[0]+offset[0]+(markerCorners[0][1]-center[1])*coef_x, y=pos[1]+offset[1]+(markerCorners[0][0]-center[0])*coef_y, z=2, f = 3000)
            anycubic.move_axis(x=pos[0]+offset[0]+(markerCorners[1][1]-center[1])*coef_x, y=pos[1]+offset[1]+(markerCorners[1][0]-center[0])*coef_y, z=2, f = 3000)
            anycubic.move_axis(x=pos[0]+offset[0]+(markerCorners[2][1]-center[1])*coef_x, y=pos[1]+offset[1]+(markerCorners[2][0]-center[0])*coef_y, z=2, f = 3000)
            anycubic.move_axis(x=pos[0]+offset[0]+(markerCorners[3][1]-center[1])*coef_x, y=pos[1]+offset[1]+(markerCorners[3][0]-center[0])*coef_y, z=2, f = 3000)
            anycubic.move_axis(x=pos[0]+offset[0]+(markerCorners[0][1]-center[1])*coef_x, y=pos[1]+offset[1]+(markerCorners[0][0]-center[0])*coef_y, z=2, f = 3000)
            anycubic.move_axis(x=100, y=100, z=100, f = 8000)
                    
        if key == 27: 
            cv2.destroyAllWindows()
            print('f ', f, ' z_offset ', z_offset)
            break
       
    
    pickle.dump(z_offset, open('Platform/Calibration/z_offset.pkl', 'wb'))
    pickle.dump(f, open('Platform/Calibration/f.pkl', 'wb'))
   