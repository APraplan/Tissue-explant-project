import platform
if platform.system() == 'Windows':
    import serial.tools.list_ports
    from pygrabber.dshow_graph import FilterGraph
    import logging

    log = logging.getLogger(__name__)

    def list_com_ports()-> None:
        """
        List all the available COM ports and their description.
        """
        port_data: list = list()
        
        for port in serial.tools.list_ports.comports():
            info = dict({"Name": port.name, "Description": port.description, "Manufacturer": port.manufacturer,
                    "Hwid": port.hwid})
            port_data.append(info)
                
        if len(port_data) == 0:
            logging.info("No COM port found")
        else:
            logging.info(port_data)
            
    
    def list_cam_index()-> None:
        """
        List all the available cameras and their index.
        """
        available_cameras: dict = dict()

        os.environ["OPENCV_LOG_LEVEL"]="SILENT"
        max_numbers_of_cameras_to_check = 10
        for index in range(max_numbers_of_cameras_to_check):
            capture = cv2.VideoCapture(index)
            if capture.read()[0]:
                camera_name = subprocess.run(['cat', '/sys/class/video4linux/video{}/name'.format(index)],
                                            stdout=subprocess.PIPE).stdout.decode('utf-8')
                camera_name = camera_name.replace('\n', '')
                available_cameras[index] = camera_name
        
        if len(available_cameras) == 0:
            logging.info("No camera found")
        else:
            logging.info(available_cameras)
        
    
    def get_com_port(VID, PID)-> str:
        """Return the COM port of the device corresponding the VID and PID givven.

        Args:
            VID (string): USB Vendor ID.
            PID (string): USB Product ID.

        Returns:
            str: COM port of the device corresponding the VID and PID.
        """
        coresponding_port: list = list()
        
        for port in serial.tools.list_ports.comports():
            port_VID = port.hwid.replace("USB VID:PID=", "")[:4]
            port_PID = port.hwid.replace("USB VID:PID=", "")[5:9]
            
            if port_VID == VID and port_PID == PID:
                coresponding_port.append(port.name)
                
        if len(coresponding_port) == 0:
            logging.error("No COM port found for VID: {} and PID: {}".format(VID, PID))
        elif len(coresponding_port) > 1:
            logging.error("More than one COM port found for VID: {} and PID: {}".format(VID, PID))
        else:
            return coresponding_port[0]
            
        
    def get_cam_index(name)-> int:
        """Return the index of the camera corresponding the name givven.

        Args:
            name (string): Name of the camera.

        Returns:
            int: Index of the camera corresponding the name givven.
        """
        corresponding_port: list = list() 
        
        for device_index, device_name in enumerate(FilterGraph().get_input_devices()):        
            if device_name == name:
                corresponding_port.append(device_index)
                    
        if len(corresponding_port) == 0:
            logging.error("No camera found for name: {}".format(name))
        elif len(corresponding_port) > 1:
            logging.error("More than one camera found for name: {}".format(name))
        else:
            return corresponding_port[0]


elif platform.system() == 'Linux':
    import os
    os.environ["OPENCV_LOG_LEVEL"]="FATAL"
    import serial.tools.list_ports
    import subprocess
    import cv2
    import logging

    log = logging.getLogger(__name__)

    def list_com_ports()-> None:
        """
        List all the available COM ports and their description.
        """
        port_data: list = list()
        
        for port in serial.tools.list_ports.comports():
            info = dict({"Name": port.name, "Description": port.description, "Manufacturer": port.manufacturer,
                    "Hwid": port.hwid})
            port_data.append(info)
                
        if len(port_data) == 0:
            logging.info("No ttyUSB port found")
        else:
            logging.info(port_data)
            
        
    def list_cam_index()-> None:
        """
        List all the available cameras and their index.
        """
        available_cameras: dict = dict()

        max_numbers_of_cameras_to_check = 10
        for index in range(max_numbers_of_cameras_to_check):
            capture = cv2.VideoCapture(index)
            if capture.read()[0]:
                camera_name = subprocess.run(['cat', '/sys/class/video4linux/video{}/name'.format(index)],
                                            stdout=subprocess.PIPE).stdout.decode('utf-8')
                camera_name = camera_name.replace('\n', '')
                available_cameras[index] = camera_name
        
        if len(available_cameras) == 0:
            logging.info("No camera found")
        else:
            logging.info(available_cameras)
            
        
    def get_com_port(VID, PID)-> str:
        """Return the COM port of the device corresponding the VID and PID givven.

        Args:
            VID (string): USB Vendor ID.
            PID (string): USB Product ID.

        Returns:
            str: COM port of the device corresponding the VID and PID.
        """
        coresponding_port:list = list()
            
        for port in serial.tools.list_ports.comports():
            port_VID = port.hwid.replace("USB VID:PID=", "")[:4]
            port_PID = port.hwid.replace("USB VID:PID=", "")[5:9]
            
            if port_VID == VID and port_PID == PID:
                coresponding_port.append(port.name)
                
        if len(coresponding_port) == 0:
            logging.error("No ttyUSB port found for VID: {} and PID: {}".format(VID, PID))
        elif len(coresponding_port) > 1:
            logging.error("More than one ttyUSB port found for VID: {} and PID: {}".format(VID, PID))
        else:
            return '/dev/' + coresponding_port[0]
        
        
    def get_cam_index(name)-> int:
        """Return the index of the camera corresponding the name givven.

        Args:
            name (string): Name of the camera.

        Returns:
            int: Index of the camera corresponding the name givven.
        """
        corresponding_port: list = list() 
        max_numbers_of_cameras_to_check = 10

        for device_index in range(max_numbers_of_cameras_to_check):
            capture = cv2.VideoCapture(device_index)
            if capture.read()[0]:
                camera_name = subprocess.run(['cat', '/sys/class/video4linux/video{}/name'.format(device_index)],
                                            stdout=subprocess.PIPE).stdout.decode('utf-8')
                camera_name = camera_name.replace('\n', '')
                if camera_name[:len(name)] == name:
                    corresponding_port.append(device_index)

        if len(corresponding_port) == 0:
            logging.error("No camera found for name: {}".format(name))
        elif len(corresponding_port) > 1:
            logging.error("More than one camera found for name: {}".format(name))
        else:
            return corresponding_port[0]     


if __name__ == '__main__':
    
    logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
    
    list_com_ports()
    list_cam_index()
    
# print(get_com_port("0403", "6014"))
# print(get_com_port("0403", "6001"))
# print(get_cam_index("TV Camera"))
    
# "0403", "6014" Dynamixel controller
# "0403", "6001" GRBL controller
# "1A86", "7523" Anycubic mega zero