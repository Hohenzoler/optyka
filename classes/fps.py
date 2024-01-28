import win32api
from win32com.client import GetObject

try:
    device_info = win32api.EnumDisplayDevices()
except:
    pass

def refresh_rate(device):
    try:
        settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
        return settings.DisplayFrequency
    except:
        return 60
def gpuInfo(device):
    try:
        return((device.DeviceString))
    except:
        return "GPU not found"

def get_cpu_type():
    try:
        root_winmgmts = GetObject("winmgmts:root\cimv2")
        cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
        return cpus[0].Name
    except:
        return "CPU not found"


# print(f"User's refresh rate: {refresh_rate(device_info)}")
# print(f"User's GPU: {gpuInfo(device_info)}")
# print(f"User's CPU: {get_cpu_type()}")

def return_fps():
    return refresh_rate(device_info)+1