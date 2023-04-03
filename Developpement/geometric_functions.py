import numpy as np
import math
      
def intersection_line_plan(l, l0, n, p0):
    l_n = np.dot(l, n)
    if(l_n == 0):
        print('Line and plan parallel')
        return
    else:
        d = np.dot(p0 - l0, n)/l_n
        return l0 + d * l
        
def intermediate_point_plan(x1, y1, x2, y2, min_x, max_x, min_y, max_y, safe_z):
    
    l = np.array([x2-x1, y2-y1])
    l0 = np.array([x2, y2])
    
    if x1 <= min_x:
        n = np.array([1, 0])
        p0 = np.array([min_x, 0])
        
    elif x1 >= max_x:
        n = np.array([1, 0])
        p0 = np.array([max_x, 0])
        
    elif y1 <= min_y:
        n = np.array([0, 1])
        p0 = np.array([0, min_y])
    
    elif y1 >= max_y:
        n = np.array([0, 1])
        p0 = np.array([0, max_y])
        
    else:
        return x2, y2, safe_z
    
    p_int = intersection_line_plan(l, l0, n, p0)

    return int(p_int[0]), int(p_int[1]), safe_z

    
def intermediate_point_cylinder(x1, y1, x2, y2, R, safe_z):
    
    a = math.atan2(y1-y2, x1-x2)
    
    return int(R*math.cos(a)+x2), int(R*math.sin(a)+y2), safe_z
       