
RESET = 0
DETECT = 1
PICK = 2
PLACE = 3
PAUSE = 4

SBD = 0
TM = 1


class PlatformParameters:
    def __init__(self):
        self.status = PlatformStatus()
        self.vision = PlatformVision()
        self.movement = PlatformMovement()
        self.pipette = PlatformPipette()
    
    
class PlatformStatus:
     def __init__(self):
        self.state = RESET
        self.collected_samples = 0
        self.remaining_sample = None
        self.average_attemtp = 0
        
        
class PlatformVision:
     def __init__(self):
        self.offset_cam = (-24, -13)
         
        # Public
        self.size_min = 50
        self.size_max = 150
        self.detection_type = SBD   
        
        
class PlatformMovement:
    def __init__(self):
        self.height_pick = 0.8
        
        # Public
        self.speed_tracking = 30
        self.speed_empty = 80
        self.speed_on_load = 10
        
        
class PlatformPipette:
    def __init__(self):
        
        # Public
        self.volume_pick = 70
        self.volume_place = 10
        self.speed_pumping = 20
        self.speed_blowing = 50
        self.pumping_on_move = False
        
        
class Sample:
    
    def __init__(self, num, x, y, image = None):
        self.num = num
        self.x = x
        self.y = y
        self.image = None
        
