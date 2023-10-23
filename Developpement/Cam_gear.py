# import required libraries
from vidgear.gears import VideoGear
import cv2
import time

# define and start the stream on first source ( For e.g #0 index device)
options = {
    "CAP_PROP_FRAME_WIDTH": 1080,
    "CAP_PROP_FRAME_HEIGHT": 720,
    "CAP_PROP_FPS": 30,
}

stream1 = VideoGear(source=0, logging=True, **options).start() # prend bcp de temps, voir si c'est normal et si on peut speed up

stream2 = VideoGear(source=1, logging=True, **options).start() 

frameA = stream1.read()
frameB = stream2.read()
out1 = cv2.VideoWriter(r'Pictures\Videos\video_exp_1.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frameA.shape[1], frameA.shape[0]))
out2 = cv2.VideoWriter(r'Pictures\Videos\video_exp_0.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frameB.shape[1], frameB.shape[0]))

# infinite loop
while True:
    
    frameA = stream1.read()

    frameB = stream2.read()

    # check if any of two frame is None
    if frameA is None or frameB is None:
        #if True break the infinite loop
        break
    
    out1.write(frameA)
    out2.write(frameB)
    
    # do something with both frameA and frameB here
    cv2.imshow("Output Frame1", frameA)
    cv2.imshow("Output Frame2", frameB)
    # Show output window of stream1 and stream 2 seperately

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        #if 'q' key-pressed break out
        break
    

cv2.destroyAllWindows()
# close output window

out1.release()
out2.release()


# safely close both video streams
stream1.stop()
stream2.stop()



# ##################################

# import cv2
# import threading

# class camThread(threading.Thread):
#     def __init__(self, previewName, camID):
#         threading.Thread.__init__(self)
#         self.previewName = previewName
#         self.camID = camID
#     def run(self):
#         print( "Starting " + self.previewName)
#         camPreview(self.previewName, self.camID)

# def camPreview(previewName, camID):
#     cv2.namedWindow(previewName)
#     cam = cv2.VideoCapture(camID)
#     if cam.isOpened():  # try to get the first frame
#         rval, frame = cam.read()
#     else:
#         rval = False

#     while rval:
#         cv2.imshow(previewName, frame)
#         rval, frame = cam.read()
#         key = cv2.waitKey(20)
#         if key == 27:  # exit on ESC
#             break
#     cv2.destroyWindow(previewName)

# # Create two threads as follows
# thread1 = camThread("Camera 1", 0)
# thread2 = camThread("Camera 2", 1)
# thread1.start()
# thread2.start()