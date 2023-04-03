import threading as th
from time import time, sleep

class multithreading:
    
    def __init__(self):
        self.str = 'wesh'
    
    def start(self):
        self.__thread1 = th.Thread(target=self.__fct1)
        self.__thread2 = th.Thread(target=self.__fct2)
        self.__thread1.start()
        self.__thread2.start()

    def __fct1(self):
        while True:
            print('1')
            sleep(0.5)
            
    def __fct2(self):
        while True:
            print('2', self.str)
            sleep(0.5)


node = multithreading()
node.start()

sleep(5)

node.str = 'noooon'
