import cv2
import matplotlib as plt
import numpy as np
# from skimage import measure, color
import pickle
import math

# def get_cell_position():
#     return tissue(50, 105, 10)


WIDTH_PX = 1146
HEIGHT_PX = 530
WIDHT_MM = 210
HEIGHT_MM = 95.7
RATIO_X = WIDHT_MM/WIDTH_PX # 0.1832 = 1/5.457
RATIO_Y = HEIGHT_MM/HEIGHT_PX # 0.1805 = 1/5.538
# OFFSET_X = -12.4
# OFFSET_Y = 20.4
# ANGLE = 0.0175


YELLOW = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)


def d_circle(img, keypoints, radius, color):
    
    thickness = 1

    for i in range(len(keypoints)):
            out = cv2.circle(img, (int(keypoints[i].pt[0]),int(keypoints[i].pt[1])), radius, color, thickness)      
    
    return img
    
    
def d_number(img, keypoints, color):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    thickness = 1

    for i in range(len(keypoints)):
            size, _ = cv2.getTextSize(str(i+1), font, fontScale, thickness)
            img = cv2.putText(img, str(i+1), (int(keypoints[i].pt[0]-size[0]/2),int(keypoints[i].pt[1]-5)), font, 
                    fontScale, color, thickness, cv2.LINE_AA)
    
    return img

def d_angles(img, keypoint, angles, color):
        
    thickness = 1  
    length = 30
      
    for i in range(len(angles)):
        end_point = (int(keypoint.pt[0]+length*math.cos(angles[i])), int(keypoint.pt[1]+length*math.sin(angles[i])))
        img = cv2.line(img, (int(keypoint.pt[0]),int(keypoint.pt[1])), end_point, color, thickness)   
    
    return img  

def make_720p(cap):
    cap.set(3, 1280)
    cap.set(4, 720)


class Camera:
    def __init__(self, img):
        
        cameraMatrix = pickle.load(open('Platform/Calibration/cameraMatrix.pkl', 'rb'))
        dist = pickle.load(open('Platform/Calibration/dist.pkl', 'rb'))
        
        self.offset = pickle.load(open('Platform/Calibration/offset.pkl', 'rb'))
        self.angle = pickle.load(open('Platform/Calibration/angle.pkl', 'rb'))
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
        
        x = position[0]+self.offset[0] + np.cos(self.angle)*((coord[1]-self.center[1])*coef_x)-np.sin(self.angle)*((coord[0]-self.center[0])*coef_y)
        y = position[1]+self.offset[1] + np.sin(self.angle)*((coord[1]-self.center[1])*coef_x)+np.cos(self.angle)*((coord[0]-self.center[0])*coef_y)      
            
        return [x, y]


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

def mask_pipette(self):

    image = self.frame.copy()
    color = (0,0,0)
    thickness = -1
    radius = 7
    
    p1 = [605, 525]
    p2 = [670, 525]

    cv2.line(image, self.pipette_pos_px, p1, color, 12)
    cv2.line(image, self.pipette_pos_px, p2, color, 12)
    cv2.line(image, self.pipette_pos_px, ((p1[0]+p2[0])//2,(p1[1]+p2[1])//2), color, 12)
    cv2.line(image, self.pipette_pos_px, ((2*p1[0]+p2[0])//3,(2*p1[1]+p2[1])//3), color, 12)
    cv2.line(image, self.pipette_pos_px, ((p1[0]+2*p2[0])//3,(p1[1]+2*p2[1])//3), color, 12)
    cv2.line(image, self.pipette_pos_px, ((4*p1[0]+p2[0])//5,(4*p1[1]+p2[1])//5), color, 12)
    cv2.line(image, self.pipette_pos_px, ((p1[0]+4*p2[0])//5,(p1[1]+4*p2[1])//5), color, 12)
    cv2.circle(image, self.pipette_pos_px, radius, color, thickness)
    
    cv2.imshow('mask', image)

    return image

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

def create_sample_detector():
    
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

        # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 200


    # Filter by Area.
    params.filterByArea = True
    params.minArea = 50
    params.maxArea = 70

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.8

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.3

    # Create a detector with the parameters
    # OLD: detector = cv2.SimpleBlobDetector(params)
    detector = cv2.SimpleBlobDetector_create(params)
    
    return detector

def create_intruder_detector():
    
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 240


    # Filter by Area.
    params.filterByArea = True
    params.minArea = 30
    params.maxArea = 500

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.8

    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.5
    
    # Create a detector with the parameters
    # OLD: detector = cv2.SimpleBlobDetector(params)
    detector = cv2.SimpleBlobDetector_create(params)
    
    return detector


def distance(keypoint1, keypoint2):
    return math.sqrt((keypoint1.pt[0]-keypoint2.pt[0])**2 + (keypoint1.pt[1]-keypoint2.pt[1])**2)

# def create_real_detector():
    
#     # Setup SimpleBlobDetector parameters.
#     params = cv2.SimpleBlobDetector_Params()

#     # Change thresholds
#     params.minThreshold = 10
#     params.maxThreshold = 200


#     # Filter by Area.
#     params.filterByArea = True
#     params.minArea = 55
#     params.maxArea = 70

#     # Filter by Circularity
#     params.filterByCircularity = False
#     params.minCircularity = 0.1

#     # Filter by Convexity
#     params.filterByConvexity = True
#     params.minConvexity = 0.8

#     # Filter by Inertia
#     params.filterByInertia = True
#     params.minInertiaRatio = 0.5

#     # Create a detector with the parameters
#     # OLD: detector = cv2.SimpleBlobDetector(params)
#     detector = cv2.SimpleBlobDetector_create(params)
    
#     return detector


def detection(self):
    
    out = self.frame.copy()
    cv2.imwrite("Pictures\detection\image.png", out)
    
    zoi = cv2.bitwise_and(self.invert, self.invert, mask=self.mask)

    # Detect blobs.
    keypoints = self.sample_detector.detect(zoi)
    keypoints_intruders = self.intruder_detector.detect(zoi)

    out = d_circle(out, keypoints, 5, YELLOW)

    smallest_distances = []
    close_angles = []
    i = 0

    while i < len(keypoints):
        
        angles = []
        nb_too_close = 0
        smallest_dist = self.max_radius
        
        for j in range(len(keypoints_intruders)):
            
            dist = distance(keypoints[i], keypoints_intruders[j])
            
            if dist < self.min_radius:
                nb_too_close += 1
                
            elif dist < self.max_radius:
                if dist < smallest_dist:
                    smallest_dist = dist
                    
                angles.append(math.atan2((keypoints_intruders[j].pt[1]-keypoints[i].pt[1]), (keypoints_intruders[j].pt[0]-keypoints[i].pt[0])))
                
        # If elements too close remove keypoint, else keep the close elements on the table 
        if nb_too_close <= 1:
            angles.sort()
            close_angles.append(angles)
            smallest_distances.append(smallest_dist)
            i += 1
        else:
            keypoints = tuple(item for item in keypoints if item != keypoints[i])
            
    if len(keypoints) == 0:
        return None, None
       
    out = d_number(out, keypoints, YELLOW)
    out = d_circle(out, keypoints, self.max_radius, YELLOW)  
    
    for i in range(len(keypoints)):
        out = d_angles(out, keypoints[i], close_angles[i], RED)  
                
        id_target = smallest_distances.index(max(smallest_distances))
        angles = close_angles[id_target]
        angles_diff = []
        if len(angles) > 0:
            for i in range(len(angles)-1):
                angles_diff.append(angles[i+1]-angles[i])
            angles_diff.append(2*math.pi+angles[0]-angles[-1])

            id_angle = angles_diff.index(max(angles_diff))
            optimal_angle = angles[id_angle]+angles_diff[id_angle]/2.0
        else:
            optimal_angle = math.pi/4.0
            
        
        optimal_angle = (optimal_angle + 3*math.pi) %  (2*math.pi) - math.pi
        
        if optimal_angle < 0:
            if optimal_angle < -math.pi/2.:
                optimal_angle = math.pi
            else:
                optimal_angle = 0
            
        # if optimal_angle < -3.*math.pi/8.:
        #     if optimal_angle < -3.*math.pi/4.:
        #         optimal_angle = math.pi
        #     else:
        #         optimal_angle = -3.*math.pi/8.

        out = d_angles(out, keypoints[id_target], [optimal_angle], GREEN)   
        out = d_circle(out, [keypoints[id_target]], 5, GREEN)
        
    cv2.imwrite("Pictures\detection\image_detection.png", out)
        
    return [keypoints[id_target].pt[0], keypoints[id_target].pt[1]], optimal_angle
        
    
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
    