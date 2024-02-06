import cv2
import threading
import sys
import time
sys.path.append("Platform")
from Platform.Communication.ports_gestion import *


class camThread(threading.Thread):    
    def __init__(self, previewName, camID, preview = False):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.readyFlag = True
        self.ready = False
        
        self.frame = None  # The current pbm is that we are saving the img at every itteration.... It can take up a lot of resources.
        
        self.closing = False # Variable to be externally controlled for manually closing the thread
        self.preview = preview # Variable to be externally controlled for managing the window's visibility
        self._isWindowClosed = True  # Internal variable defining the status of the window.
        
    def run(self):
        print( "Starting " + self.previewName)
        self.camPreview()
                
    def read(self): 
        #resize frame 
        return self.frame
        
    def stop(self):
        self.preview = False
        self.closing = True
        
    def camPreview(self):
        cam = cv2.VideoCapture(self.camID, cv2.CAP_DSHOW)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        if cam.isOpened():  # try to get the first frame
            rval, self.frame = cam.read()
        else:
            rval = False
            print("Error getting frame for ", self.previewName)

        while rval:
            self.windowManagement()
            if self.readyFlag ==True:
                print("camera is ready") 
                self.ready = True
                self.readyFlag = False
            if not self._isWindowClosed: # peut-être moyen de mettre dans la fonction window management
                cv2.imshow(self.previewName, self.frame)
            rval, self.frame = cam.read()
            key = cv2.waitKey(20)
            if key == 27 or self.closing:  # exit on ESC
                self.preview = False
                break
        self.windowManagement() 
        # ATTENTION, il n'y a pas de moyen d'arrêté le thread si le closing n'est pas codé et que les fenêtres sont fermées!
       
    def windowManagement(self): 
        if self._isWindowClosed and self.preview:
            cv2.namedWindow(self.previewName)
            self._isWindowClosed = False
            print("Openning video feed from " + self.previewName)
        if not(self._isWindowClosed or self.preview):
            cv2.destroyWindow(self.previewName)    
            self._isWindowClosed = True 
            print("Closing video feed from " + self.previewName)

def get_cam_frame(cam):  # function to be called externally to get the frame.
    while not cam.ready:
        None
    return cam.read()


if __name__ == "__main__":
    
    # Create two threads as follows
    thread1 = camThread("Camera 1", get_cam_index("TV Camera"), preview = True) 
    # thread2 = camThread("Camera 2", get_cam_index("USB2.0 UVC PC Camera"), preview = True)
    thread1.start()
    # thread2.start()
    time.sleep(30)
