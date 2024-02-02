# Importing necessary libraries
try:
    import win32api
    from win32com.client import GetObject
except:
    pass

# Attempt to get device information
try:
    device_info = win32api.EnumDisplayDevices()
except:
    pass

def refresh_rate(device):
    """
    Function to get the refresh rate of the device.

    Args:
        device: The device for which the refresh rate is to be found.

    Returns:
        The refresh rate of the device. If an error occurs, it returns 60.
    """
    try:
        settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
        return settings.DisplayFrequency
    except:
        return 60

def gpuInfo(device):
    """
    Function to get the GPU information of the device.

    Args:
        device: The device for which the GPU information is to be found.

    Returns:
        The GPU information of the device. If an error occurs, it returns "GPU not found".
    """
    try:
        return((device.DeviceString))
    except:
        return "GPU not found"

def get_cpu_type():
    """
    Function to get the CPU type of the device.

    Returns:
        The CPU type of the device. If an error occurs, it returns "CPU not found".
    """
    try:
        root_winmgmts = GetObject("winmgmts:root\cimv2")
        cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
        return cpus[0].Name
    except:
        return "CPU not found"

def return_fps():
    """
    Function to get the frames per second (fps) of the device.

    Returns:
        The fps of the device. If an error occurs, it tries to get the fps for "amogus" and returns that.
    """
    try:
        return refresh_rate(device_info)+1
    except:
        return refresh_rate("amogus")+1