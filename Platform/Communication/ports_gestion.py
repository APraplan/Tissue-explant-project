import serial.tools.list_ports
from pygrabber.dshow_graph import FilterGraph

def list_com_ports()-> None:
    """
    List all the available COM ports and their description.
    """
    port_data = []
    
    for port in serial.tools.list_ports.comports():
        info = dict({"Name": port.name, "Description": port.description, "Manufacturer": port.manufacturer,
                 "Hwid": port.hwid})
        port_data.append(info)
            
    print (port_data)
    
def list_cam_ports()-> None:
    """
    List all the available cameras and their index.
    """
    available_cameras = {}

    for device_index, device_name in enumerate(FilterGraph().get_input_devices()):
        available_cameras[device_index] = device_name
    
    print (available_cameras)
        
def get_com_ports(name_list)-> dict:
    """
    Return a dictionary with the COM ports of the devices in name_list.

    Args:
        name_list (String): Name of the devices to find.

    Returns:
        dict: Dictionary with the COM ports of the devices in name_list.
    """
    port_data = {}
    
    for port in serial.tools.list_ports.comports():
        for name in name_list:
            if port.description[:len(name)] == name:
                port_data[name] = port.name
                
    return port_data

def get_cam_ports(name_list)-> dict:
    """
    Return a dictionary with the index of the cameras in name_list.

    Args:
        name_list (String): Name of the cameras to find.

    Returns:
        dict: Dictionary with the index of the cameras in name_list.
    """
    
    port_data = {}
    
    for device_index, device_name in enumerate(FilterGraph().get_input_devices()):
        for name in name_list:
            if device_name == name:
                port_data[name] = device_index
                
    return port_data

if __name__ == '__main__':
    list_com_ports()
    list_cam_ports()