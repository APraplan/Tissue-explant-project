import sys
sys.path.append('c:/Users/APrap/Documents/CREATE/Pick-and-Place/Platform')
import cv2
import computer_vision as cv

detector = cv.create_detector()
tracker = cv2.TrackerCSRT.create()

cap = cv2.VideoCapture(0)
roi_size = 40

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
color = (255, 0, 0)
thickness = 1

mask = cv.create_mask(200, (480, 640), (320, 240))

track_on = False

while True:
    
    ret, frame = cap.read()
    
    imshow = frame.copy()
    zoi = cv2.bitwise_and(frame, frame, mask=mask)
    
    if track_on:
        success, bbox = tracker.update(frame) 
        if success:
            x, y, w, h = [int(i) for i in bbox]
            cv2.rectangle(imshow, (x, y), (x + w, y + h), (0, 255, 0), 2) 
    
    keypoints = detector.detect(zoi)
           
    if len(keypoints) > 0:
        target = [keypoints[0].pt[1], keypoints[0].pt[0]] 
        # bbox = [int(target[1]-roi_size/2),int(target[0]-roi_size/2), roi_size, roi_size]
        # x, y, w, h = [int(i) for i in bbox]
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) 
    else:
        target = None

    for i in range(len(keypoints)):
            size, _ = cv2.getTextSize(str(i+1), font, fontScale, thickness)
            imshow = cv2.putText(imshow, str(i+1), (int(keypoints[i].pt[0]-size[0]/2),int(keypoints[i].pt[1]-5)), font, 
                    fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow('Camera', imshow)
    cv2.imshow('Cam', frame)
    cv2.imshow('m', mask)

    k = cv2.waitKey(5) & 0xFF
    
    if k == ord('t'):
        if track_on:
            break
        track_on = True        
        bbox = [int(target[1]-roi_size/2),int(target[0]-roi_size/2), roi_size, roi_size]
        tracker.init(frame, bbox)
        
    if k == ord('r'):
        track_on = False        
        tracker = cv2.TrackerKCF.create()
    
    if k == 27: 
        break