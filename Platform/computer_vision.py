import cv2
import matplotlib as plt
import numpy as np
# from skimage import measure, color

# def get_cell_position():
#     return tissue(50, 105, 10)


WIDHT_PX = 640
HEIGHT_PX = 480
WIDHT_CM = 12
HEIGHT_CM = 8
RATIO_X = WIDHT_CM/WIDHT_PX
RATIO_Y = HEIGHT_CM/HEIGHT_PX
OFFSET_X = 10
OFFSET_Y = -10 


def get_position2(image):
    # cv2.imshow('Image', image)
    # cv2.waitKey(0) 
    
    image_blur = cv2.GaussianBlur(image, (5,5), 0)
    # cv2.imshow('Image', image_blur)
    # cv2.waitKey(0) 
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    laplacien = np.uint8(np.absolute(cv2.Laplacian(gray_image, cv2.CV_64F)))
    # cv2.imshow('Image', laplacien)
    # cv2.waitKey(0) 
    
    min = int(np.min(laplacien)+25)
    max = int(np.max(laplacien)-5)
    binary = cv2.inRange(laplacien, min, max)
    # cv2.imshow('Binary', binary)
    # cv2.waitKey(0) 
    
    # dilated = cv2.dilate(binary, (100,100), cv2.MORPH_RECT)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=2)
    erroded = cv2.erode(dilated, kernel, iterations=2)
    # cv2.imshow('Dilated', dilated)
    # cv2.waitKey(0) 
    
    # labels = measure.label(erroded)
    # cv2.imshow('Dilated', labels)
    cv2.waitKey(0) 

image = cv2.imread('Pictures/image6.png')


def detection_test(image, mask):
        
    zoi = cv2.bitwise_and(image, image, mask=mask)
    
    out = image.copy()

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 200


    # Filter by Area.
    params.filterByArea = True
    params.minArea = 30
    params.maxArea = 500

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    # OLD: detector = cv2.SimpleBlobDetector(params)
    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(zoi)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
    # the size of the circle corresponds to the size of blob

    # im_with_keypoints = cv2.drawKeypoints(gray_image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (0, 255, 0)
    thickness = 1

    # for i in range(len(keypoints)):
    #         size, _ = cv2.getTextSize(str(i+1), font, fontScale, thickness)
    #         out = cv2.putText(out, str(i+1), (int(keypoints[i].pt[0]-size[0]/2),int(keypoints[i].pt[1]-5)), font, 
    #                 fontScale, color, thickness, cv2.LINE_AA)
    
    radius = 10
    color = (0, 255, 0)
    thickness = 1
    
    for i in range(len(keypoints)):
        out = cv2.circle(out, (int(keypoints[i].pt[0]),int(keypoints[i].pt[1])), radius, color, thickness)
            
    return out


def create_mask(radius, shape, center_coordinates):
    mask = np.zeros(shape, dtype='uint8')
    color = 255
    thickness = -1
    return cv2.circle(mask, center_coordinates, radius, color, thickness)


def create_detector():
    
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 200


    # Filter by Area.
    params.filterByArea = True
    params.minArea = 30
    params.maxArea = 500

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    # OLD: detector = cv2.SimpleBlobDetector(params)
    detector = cv2.SimpleBlobDetector_create(params)
    
    return detector 
    
    

def detect(image, position, detector, mask = None):
    
    if mask is not None:
        zoi = cv2.bitwise_and(image, image, mask=mask)
    else:
        zoi = image
    
    keypoints = detector.detect(zoi)
    
       
    if len(keypoints) > 0:
        target = (position[0]+OFFSET_Y+keypoints[0].pt[1]*RATIO_Y, position[1]+OFFSET_X+keypoints[0].pt[1]*RATIO_X) 
    else:
        target = None
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (255, 0, 0)
    thickness = 1
    
    for i in range(len(keypoints)):
        size, _ = cv2.getTextSize(str(i+1), font, fontScale, thickness)
        image = cv2.putText(image, str(i+1), (int(keypoints[i].pt[0]-size[0]/2),int(keypoints[i].pt[1]-5)), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    
    cv2.imwrite("Pictures\detection\image.png", image)
    
    return target


def check_pickup(image, detector):
    
    return True
    
    zoi = image[:,:]
    
    keypoints = detector.detect(zoi)
    
    if keypoints is not None:
        return True
    else:
        return False


# def pick_and_place():
    
#     cap = cv2.VideoCapture(0) 

#     # Check if camera opened successfully
#     if not cap.isOpened():
#         print("Error opening video stream or file")
           
#     while True:
        
#         _, frame = cap.read()                 
        
#         # Display   
#         imshow = platform.print(frame)   
#         cv2.imshow('Camera', imshow) 


    
#         sleep(0.05)
        
#     cap.release() 
#     cv2.destroyAllWindows()