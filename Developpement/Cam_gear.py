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
stream1 = VideoGear(source=0, logging=True, **options).start() 

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
    
    out1.write(self.frameA)
    out2.write(self.frameB)
    
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