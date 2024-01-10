import win32api
from win32com.client import GetObject
device_info = win32api.EnumDisplayDevices()

def refresh_rate(device):
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    return settings.DisplayFrequency

def gpuInfo(device):
    return((device.DeviceString))

def get_cpu_type():
    root_winmgmts = GetObject("winmgmts:root\cimv2")
    cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
    return cpus[0].Name


print(f"User's refresh rate: {refresh_rate(device_info)}")
print(f"User's GPU: {gpuInfo(device_info)}")
print(f"User's CPU: {get_cpu_type()}")

def return_fps():
    return refresh_rate(device_info)