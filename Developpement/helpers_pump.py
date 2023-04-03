import time
from time import sleep

def Pump(direction,pump_time,speed,arduino_instance):

    '''direction: Suck= -1, Eject= 1, Stop=0'''

    arduino = arduino_instance

    start_message = str(direction)+"@"+str(speed)  # Arduino debug scripts uses this form
    stop_message = str(0)+"@"+str(speed) # speed does not matter here

    echo_python_msg = None
    echo_python_msg = arduino.debug()
    start_time_command = time.time()
    i = 0
    while echo_python_msg != start_message:
        i += 0
        arduino.send_message([direction,speed])  # form that arduino takes the message as a list
        start_time = time.time()
        echo_python_msg = arduino.debug()
        if echo_python_msg == start_message:
            print("Message Delivered in --- %s seconds ---" % (time.time() - start_time))
            print("Output: " + echo_python_msg + ", # Sent Msgs:" + str(i))

    sleep(pump_time)

    i = 0
    while echo_python_msg != stop_message:
        i += 0
        arduino.send_message([0,speed])
        start_time = time.time()
        echo_python_msg = arduino.debug()
        if echo_python_msg == stop_message:
            print("Message Delivered in --- %s seconds ---" % (time.time() - start_time))
            print("Output: " + echo_python_msg + ", # Sent Msgs:" + str(i))

    print("Time to send Pump command: %s seconds " % (time.time() - start_time_command))
