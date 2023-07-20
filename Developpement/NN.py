import tensorflow as tf
import cv2
from keras.models import load_model
from loguru import logger
import numpy as np
from vidgear.gears import VideoGear
import matplotlib.pyplot as plt

# image = np.expand_dims(image, axis=0)

NN = load_model(r'C:\Users\APrap\Documents\CREATE\Pick-and-Place\TEP_convNN_92')

# img = tf.convert_to_tensor(image, dtype=tf.uint8)

# # print(img.shape)
# for i in range(30):
#     image = plt.imread(r'C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\macro\macro_image_' + str(i) + '.png')
#     res = NN.predict(image.reshape(1, 480, 640, 3))
    
#     # logger.info(f'🔮 Prediciton results {round(res[0, 0], 2)}%')
#     print("🔮 Prediciton results {:0.2f}".format(res[0, 0]))
#     plt.imshow(image)
#     plt.show()
    
    
stream2 = VideoGear(source=1, logging=True).start() 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('video_0.mp4', fourcc, 20.0, (480, 640))
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))



# infinite loop
while True:

    frameB = stream2.read()
    
    res = NN.predict(cv2.cvtColor(frameB, cv2.COLOR_BGR2RGB).reshape(1, 480, 640, 3))
    print(res)
    print(f"🔮 Prediciton results {res[0, 0]}")
    print(frameB.shape)
    
    out.write(frameB)

    if frameB is None:
        break
    
    cv2.imshow("Output Frame2", frameB)

    key = cv2.waitKeyEx(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()

stream2.stop()
out.release()
