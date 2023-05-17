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

# define and start the stream on second source ( For e.g #1 index device)
stream2 = VideoGear(source=1, logging=True).start() 

# infinite loop
while True:
    
    frameA = stream1.read()
    # read frames from stream1

    frameB = stream2.read()
    # read frames from stream2

    # check if any of two frame is None
    if frameA is None or frameB is None:
        #if True break the infinite loop
        break
    
    # do something with both frameA and frameB here
    cv2.imshow("Output Frame1", frameA)
    cv2.imshow("Output Frame2", frameB)
    # Show output window of stream1 and stream 2 seperately

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        #if 'q' key-pressed break out
        break

    if key == ord("w"):
        #if 'w' key-pressed save both frameA and frameB at same time
        cv2.imwrite("Image-1.jpg", frameA)
        cv2.imwrite("Image-2.jpg", frameB)
        #break   #uncomment this line to break out after taking images

cv2.destroyAllWindows()
# close output window

# safely close both video streams
stream1.stop()
stream2.stop()