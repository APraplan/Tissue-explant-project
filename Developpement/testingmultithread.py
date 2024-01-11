import time
import cv2
import Cam_gear as cam_gear

cam1 = cam_gear.camThread("Camera 1", 0, )
cam2 = cam_gear.camThread("Camera 2", 1, )

cam1.start()
cam2.start()


# while not cam1.ready: # attendre que ca soit prêt
#     None
# time.sleep(3)
# cam1.preview = False
# print("cam1 preview off")

# while not cam2.ready:
#     None
# time.sleep(3)
# cam2.preview = False
# print("cam2 preview off")

# print("waiting another 3 seconds")
# time.sleep(3)
# cam1.preview = True
# cam2.preview = True

# print("waiting another 10 seconds before shutting down")
# time.sleep(10)

# cam1.closing = True
# cam2.closing = True

while not cam1.ready:
    None
frame = cam1.read()
while not cam2.ready:
    None
# cam1.closing = True
# cam2.closing = True

time.sleep(2)
cv2.imshow("test1.png",frame)

cam1.close()
cam2.close()
# print(giveFrame['2'])
