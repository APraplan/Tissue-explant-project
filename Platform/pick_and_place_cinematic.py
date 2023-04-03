from movement_functions import *
from Platform.computer_vision import *



# def pick_and_place():
    
#     cap = cv2.VideoCapture(0) 

#     # Check if camera opened successfully
#     if not cap.isOpened():
#         print("Error opening video stream or file")
        
#     out = cv2.VideoWriter('video.mp4', -1, 25.0, (603,427))
           
#     while True:
        
#         _, frame = cap.read() 
#         frame = cv.undistort(frame)
        
        
#         platform.run(frame) 
                
        
#         # Display   
#         imshow = platform.print(frame)   
#         cv2.imshow('Camera', imshow) 
        
#         out.write(imshow)


#         # Inputs
#         key = cv2.waitKey(10) & 0xFF    
        
#         if key == 27: #esc
#             platform.reset()
#             break
#         if key == ord('p'):
#             platform.pause()
#         if key == 13: # enter
#             platform.resume()            
    
#     cap.release() 
#     out.release()
#     cv2.destroyAllWindows()
    