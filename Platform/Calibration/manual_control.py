import sys
sys.path.append('c:/Users/APrap/Documents/CREATE/Pick-and-Place/Platform')
import cv2
from Communication.printer_communications import *

anycubic = Printer(descriptive_device_name="printer", port_name="COM15", baudrate=115200)

anycubic.connect()
anycubic.homing()


def commande(key, incr):
    
    # Speed
    if key == ord("1"):
        incr = 0.1
        print('Increment set to ', incr, ' mm')
    
    if key == ord("2"):
        incr = 1
        print('Increment set to ', incr, ' mm')
        
    if key == ord("3"):
        incr = 52
        print('Increment set to ', incr, ' mm')
        
    if key == ord("4"):
        incr = 10
        print('Increment set to ', incr, ' mm')
    
    if key == ord("5"):
        incr = 50
        print('Increment set to ', incr, ' mm')
    
    # Anycubic
    if key == ord('r'):
        anycubic.read_position(printMsg=True)
        
    if key == ord('a'):
        anycubic.move_axis_incremental(x=-incr, printMsg=False)
        
    if key == ord('d'):
        anycubic.move_axis_incremental(x=incr, printMsg=False)
        
    if key == ord('w'):
        anycubic.move_axis_incremental(y=incr, printMsg=False)
        
    if key == ord('s'):
        anycubic.move_axis_incremental(y=-incr, printMsg=False)
        
    if key == ord('e'):
        anycubic.move_axis_incremental(z=incr, printMsg=False)

    if key == ord('c'):
        anycubic.move_axis_incremental(z=-incr, printMsg=False)
        
    
    if key == ord('0'):
        anycubic.move_axis(x=75.0, y=125, z=50, f = 8000)
        
    
    return incr

incr = 10
num = 0
    
cap = cv2.VideoCapture(0) 


# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

while(True): 

    # reads frames from a camera 
    _, frame = cap.read() 
    
    markerSize = 15
    thickness = 1
    center = (frame.shape[1]//2, frame.shape[0]//2)
    frame = cv2.drawMarker(frame, center, (255, 0, 0), cv2.MARKER_CROSS, markerSize, thickness)
    
    # Display an original image 
    cv2.imshow('Camera', frame) 

    # Wait for Esc key to stop 
    k = cv2.waitKey(5) & 0xFF
    if k == ord('p'):
        # path = "C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\image" + str(num)
        cv2.imwrite("Pictures/image" + str(num) + ".png", frame)
        num += 1
        pass
    
    incr = commande(k, incr)
    

    if k == 27: 
        break
    
cap.release() 
cv2.destroyAllWindows()
    