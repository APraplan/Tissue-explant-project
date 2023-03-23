from movement_functions import *
from computer_vision import *

def pick_and_place():
    
    cap = cv2.VideoCapture(0) 

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")
           
    while True:
        
        _, frame = cap.read() 
        
        
        platform.run(frame) 
                
        
        # Display   
        imshow = platform.print(frame)   
        cv2.imshow('Camera', imshow) 


        # Inputs
        key = cv2.waitKey(10) & 0xFF    
        
        if key == 27: #esc
            platform.reset()
            break
        if key == ord('p'):
            platform.pause()
        if key == 13: # enter
            platform.resume()            
    
    cap.release() 
    cv2.destroyAllWindows()
    