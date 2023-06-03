import cv2
import numpy as np

def rounded_rectangle(src, top_left, bottom_right, radius=1, color=255, thickness=1, line_type=cv2.LINE_AA):

    #  corners:
    #  p1 - p2
    #  |     |
    #  p4 - p3

    p1 = top_left
    p2 = (bottom_right[1], top_left[1])
    p3 = (bottom_right[1], bottom_right[0])
    p4 = (top_left[0], bottom_right[0])

    height = abs(bottom_right[0] - top_left[1])

    if radius > 1:
        radius = 1

    corner_radius = int(radius * (height/2))

    if thickness < 0:

        #big rect
        top_left_main_rect = (int(p1[0] + corner_radius), int(p1[1]))
        bottom_right_main_rect = (int(p3[0] - corner_radius), int(p3[1]))

        top_left_rect_left = (p1[0], p1[1] + corner_radius)
        bottom_right_rect_left = (p4[0] + corner_radius, p4[1] - corner_radius)

        top_left_rect_right = (p2[0] - corner_radius, p2[1] + corner_radius)
        bottom_right_rect_right = (p3[0], p3[1] - corner_radius)

        all_rects = [
        [top_left_main_rect, bottom_right_main_rect], 
        [top_left_rect_left, bottom_right_rect_left], 
        [top_left_rect_right, bottom_right_rect_right]]

        [cv2.rectangle(src, rect[0], rect[1], color, thickness) for rect in all_rects]

    # draw straight lines
    cv2.line(src, (p1[0] + corner_radius, p1[1]), (p2[0] - corner_radius, p2[1]), color, abs(thickness), line_type)
    cv2.line(src, (p2[0], p2[1] + corner_radius), (p3[0], p3[1] - corner_radius), color, abs(thickness), line_type)
    cv2.line(src, (p3[0] - corner_radius, p4[1]), (p4[0] + corner_radius, p3[1]), color, abs(thickness), line_type)
    cv2.line(src, (p4[0], p4[1] - corner_radius), (p1[0], p1[1] + corner_radius), color, abs(thickness), line_type)

    # draw arcs
    cv2.ellipse(src, (p1[0] + corner_radius, p1[1] + corner_radius), (corner_radius, corner_radius), 180.0, 0, 90, color ,thickness, line_type)
    cv2.ellipse(src, (p2[0] - corner_radius, p2[1] + corner_radius), (corner_radius, corner_radius), 270.0, 0, 90, color , thickness, line_type)
    cv2.ellipse(src, (p3[0] - corner_radius, p3[1] - corner_radius), (corner_radius, corner_radius), 0.0, 0, 90,   color , thickness, line_type)
    cv2.ellipse(src, (p4[0] + corner_radius, p4[1] - corner_radius), (corner_radius, corner_radius), 90.0, 0, 90,  color , thickness, line_type)

    return src

# def print(imshow):
    
#     state = 'Idle'
#     sub_state = 'Idle'
#     well_num = 0
#     nb_sample = 0
#     nb_sample_remaning = 345
#     success = True
#     bbox = (0, 0, 25, 25)
    
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     fontScale = 0.8
#     color = (0.9, 0.9, 0.9) #BGR
#     thickness = 2
    
#     # Print state
#     text = state
#     position = [25, 240]
#     pos = position
#     # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
#     imshow = cv2.putText(imshow, text, pos, font, 
#                 fontScale, color, thickness, cv2.LINE_AA)    
    
#     text = sub_state
#     pos[1] += 40
#     # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
#     imshow = cv2.putText(imshow, text, pos, font, 
#                 fontScale, color, thickness, cv2.LINE_AA)   
    
#     text = 'Number of well ' + str(well_num) 
#     pos[1] += 40
#     imshow = cv2.putText(imshow, text, pos, font, 
#                 fontScale, color, thickness, cv2.LINE_AA)
    
#     text = 'Number of sample ' + str(nb_sample) 
#     pos[1] += 40
#     imshow = cv2.putText(imshow, text, pos, font, 
#                 fontScale, color, thickness, cv2.LINE_AA)
    
#     # text = 'Remaning samples ' + str(nb_sample_remaning) 
#     # pos[1] += 40
#     # imshow = cv2.putText(imshow, text, pos, font, 
#     #             fontScale, color, thickness, cv2.LINE_AA)
    
#     if success:
#         x, y, w, h = [int(i) for i in bbox]
#         offset = 515, 15
#         cv2.circle(imshow, (int(x+w/2+offset[0]), int(y+h/2+offset[1])), int((w+h)/4), (255, 0, 0), 2)
#         # cv2.rectangle(imshow, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    
def display(imshow, position):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0.9, 0.9, 0.9) #BGR
    thickness = 2

    fontScale = 0.8 
    
    name, unit = ['Solution B pumping volume', 'ul']
    imshow = cv2.putText(imshow, name, position, font, 
                            fontScale, color, thickness, cv2.LINE_AA)  
    
    pos = position
    pos[0] = pos[0] + 363 
    val = str(round(124.2, 2))
        
    imshow = cv2.putText(imshow, val, position, font, 
                            fontScale, color, thickness, cv2.LINE_AA)    
    
    size, _ = cv2.getTextSize(val, font, fontScale, thickness)
    pos[0] = pos[0] + size[0] + 8
    imshow = cv2.putText(imshow, unit, position, font, 
                            fontScale, color, thickness, cv2.LINE_AA)  


# Logo
mask1 = np.ones((150, 500, 3))
x = cv2.imread(r'C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\Utils\logo.png')/255
size = x.shape
format = x.shape[0]/x.shape[1]
x = cv2.resize(x, (int(150/format), 150))
size = x.shape
offset = int((500 - x.shape[1])/2)
mask1[:size[0], offset:size[1]+offset, :] = x
mask1[mask1 <= 0.5] = 0
mask1[mask1 > 0.5] = 1
mask1[mask1 == 0] = 0.9
mask1[mask1 == 1] = 0.2

# Credits
mask2 = np.ones((150, 655, 3))*0.2
mask2 = cv2.putText(mask2, 'CREATE', (mask2.shape[1]-183, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0.9, 0.9, 0.9), 3, cv2.LINE_AA)
mask2 = cv2.putText(mask2, 'lab', (mask2.shape[1]-58, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0.9, 0.9, 0.9), 2, cv2.LINE_AA)
mask2 = cv2.putText(mask2, 'by Axel Praplan', (mask2.shape[1]-136, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0.9, 0.9, 0.9), 1, cv2.LINE_AA)

# Info
mask3 = np.ones((390, 500, 3))*0.2
size= mask3.shape
mask3 = rounded_rectangle(mask3, (15, 15), (size[0]-15, size[1]-15), radius=0.1, color=(0.3, 0.3, 0.3), thickness=-1)


# Camera
mask4 = np.ones((390, 655, 3))*0.2

mask12 = np.concatenate((mask1, mask2), axis=1)
mask34 = np.concatenate((mask3, mask4), axis=1)
imshow = np.concatenate((mask12, mask34), axis=0)

cv2.imwrite(r'C:\Users\APrap\Documents\CREATE\Pick-and-Place\Backgroud.png', imshow*255)







# cam =  cv2.imread(r'C:\Users\APrap\Documents\CREATE\Pick-and-Place\image copy.png')/255
# cam = cv2.resize(cam, (640, 360))





# background = np.ones((cam.shape[0]+30, 545 + cam.shape[1], 3))*0.2
# size = background.shape
# background = rounded_rectangle(background, (15, 200), (cam.shape[0]+15, 500), radius=0.1, color=(0.3, 0.3, 0.3), thickness=-1)


# mask = np.ones_like(background)
# mask[15:size[0]+15, 20:size[1]+20, :] = x
# background[mask==0] = 0.9
# background = cv2.line(background, (40, 35), (74, 29), (0.9, 0.9, 0.9), 4)

# mask = np.ones_like(cam)
# size = cam.shape
# mask = rounded_rectangle(mask, (0, 0), (size[0], size[1]), radius=0.1, color=(0, 0, 0), thickness=-1)
# cam[mask==1] = 0.2

# background[15:size[0]+15, 515:size[1]+515, :] = cam


while True:
    
    # display(background, [25, 520])
    # print(background)
    
    cv2.imshow('Xplant', imshow)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
