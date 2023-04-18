import cv2
import matplotlib as plt
import numpy as np
# from skimage import measure, color
import pickle
import sys

# def get_cell_position():
#     return tissue(50, 105, 10)


WIDTH_PX = 1146
HEIGHT_PX = 530
WIDHT_MM = 210
HEIGHT_MM = 95.7
RATIO_X = WIDHT_MM/WIDTH_PX # 0.1832 = 1/5.457
RATIO_Y = HEIGHT_MM/HEIGHT_PX # 0.1805 = 1/5.538
OFFSET_X = -24.0
OFFSET_Y = -9.5

def make_720p(cap):
    cap.set(3, 1280)
    cap.set(4, 720)


class Camera:
    def __init__(self, img):
        
        cameraMatrix = pickle.load(open('Platform/Calibration/cameraMatrix.pkl', 'rb'))
        dist = pickle.load(open('Platform/Calibration/dist.pkl', 'rb'))
        
        self.offset = pickle.load(open('Platform/Calibration/offset.pkl', 'rb'))
        self.z_offset = pickle.load(open('Platform/Calibration/z_offset.pkl', 'rb'))
        self.f = pickle.load(open('Platform/Calibration/f.pkl', 'rb'))
        
        h,  w = img.shape[:2]
        format = float(w)/float(h)
        # print(format)
        newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

        # Undistort with Remapping
        self.mapx, self.mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
        
        # crop the image
        x, y, w, h = roi
        # print('x ', x, ' y ', y, ' w ', w, ' h ', h)
        if w/h >= format:
            self.h = h
            self.w = int(h*format)
        else:
            self.w = w
            self.h = int(w/format)
            
        self.center = (self.w//2, self.h//2)
            
        self.x = int(x+w/2-self.w/2)
        self.y = int(y+h/2-self.h/2)
        # print('self.x ', self.x, ' self.y ', self.y)
        

    def undistort(self, img):
            
        dst = cv2.remap(img, self.mapx, self.mapy, cv2.INTER_LINEAR)        
        dst = dst[self.y:self.y+self.h, self.x:self.x+self.w]
    
        return dst
    
    
    def cam_to_platform_space(self, coord, position):
        
        coef_x = (position[2] + self.z_offset)/self.f[1]
        coef_y = (position[2] + self.z_offset)/self.f[0]
            
        return [position[0]+self.offset[0]+(coord[1]-self.center[1])*coef_x, position[1]+self.offset[1]+(coord[0]-self.center[0])*coef_y]


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


def invert(image):
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_gray_image = 255 - gray_image  
    
    return inverted_gray_image


def detection_test(image, mask):
        
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_gray_image = 255 - gray_image    
        
    zoi = cv2.bitwise_and(inverted_gray_image, inverted_gray_image, mask=mask)
    
    out = image.copy()

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 200


    # Filter by Area.
    params.filterByArea = True
    params.minArea = 55
    params.maxArea = 75

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.8

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.5

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
        print(int(keypoints[i].pt[0]),int(keypoints[i].pt[1]))
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


def create_real_detector():
    
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 200


    # Filter by Area.
    params.filterByArea = True
    params.minArea = 55
    params.maxArea = 70

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.8

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.5

    # Create a detector with the parameters
    # OLD: detector = cv2.SimpleBlobDetector(params)
    detector = cv2.SimpleBlobDetector_create(params)
    
    return detector
        
    
def detect(image, detector, mask = None):
    
    cv2.imwrite("Pictures\detection\image.png", image)
    
    # Choose image
    if mask is not None:
        zoi = cv2.bitwise_and(image, image, mask=mask)
    else:
        zoi = image
    
    # Detect
    keypoints = detector.detect(zoi)
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (255, 0, 0)
    thickness = 1
    
    for i in range(len(keypoints)):
        size, _ = cv2.getTextSize(str(i+1), font, fontScale, thickness)
        image = cv2.putText(image, str(i+1), (int(keypoints[i].pt[0]-size[0]/2),int(keypoints[i].pt[1]-5)), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    
    cv2.imwrite("Pictures\detection\image_detection.png", image)
    
    # Choose keypoint
    w = 40
    h = 100
    id = 0
    valid_keypoint = False
    while not valid_keypoint:
        valid_keypoint = True    
        for i in range(len(keypoints)):
            if i == id:
                pass
            if keypoints[i].pt[0] < keypoints[id].pt[0] + w/2 and keypoints[i].pt[0] > keypoints[id].pt[0] - w/2 and \
                keypoints[i].pt[1] > keypoints[id].pt[1] and keypoints[i].pt[1] < keypoints[id].pt[1] + h:
                valid_keypoint = False
                id += 1
                break

    # Convert
    if len(keypoints) > 0:
        target_px = [keypoints[id].pt[0], keypoints[id].pt[1]]
    else:
        target_px = None 
    
    return target_px


def real_detect(image, inverted_gray_image, detector, mask):

    cv2.imwrite("Pictures\detection\image.png", image)
    
    # Choose image
    if mask is not None:
        zoi = cv2.bitwise_and(inverted_gray_image, inverted_gray_image, mask=mask)
    else:
        zoi = image
    
    # Detect
    keypoints = detector.detect(zoi)
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (255, 0, 0)
    thickness = 1
    
    for i in range(len(keypoints)):
        size, _ = cv2.getTextSize(str(i+1), font, fontScale, thickness)
        image = cv2.putText(image, str(i+1), (int(keypoints[i].pt[0]-size[0]/2),int(keypoints[i].pt[1]-5)), font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    
    cv2.imwrite("Pictures\detection\image_detection.png", image)
    
    # Choose keypoint
    w = 40
    h = 100
    id = 0
    valid_keypoint = False
    while not valid_keypoint:
        valid_keypoint = True    
        for i in range(len(keypoints)):
            if i == id:
                pass
            if keypoints[i].pt[0] < keypoints[id].pt[0] + w/2 and keypoints[i].pt[0] > keypoints[id].pt[0] - w/2 and \
                keypoints[i].pt[1] > keypoints[id].pt[1] and keypoints[i].pt[1] < keypoints[id].pt[1] + h:
                valid_keypoint = False
                id += 1
                break

    # Convert
    if len(keypoints) > 0:
        target_px = [keypoints[id].pt[0], keypoints[id].pt[1]]
    else:
        target_px = None 
    
    return target_px


def check_pickup(image, detector):
    
    return True
    
    zoi = image[:,:]
    
    keypoints = detector.detect(zoi)
    
    if keypoints is not None:
        return True
    else:
        return False 
    