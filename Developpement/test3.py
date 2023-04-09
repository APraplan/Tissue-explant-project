import time


class Timer:
    def __init__(self):
        self.chrono = 0
        self.chrono_set = False
        
    def delay(self, delay):
        
        if not self.chrono_set:
            self.chrono = delay/1000.0 + time.time()
            self.chrono_set = True
        elif time.time() >= self.chrono:
            self.chrono_set = False
            return True
        return False  
        
    def run(self):
        while True:
            if self.delay(1000):
                print('Top')
                
tim = Timer()
tim.run()