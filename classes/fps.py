import win32api

device_info = win32api.EnumDisplayDevices()

def refresh_rate(device):
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    return settings.DisplayFrequency

def gpuInfo(device):
    return((device.DeviceString))


print(f"User's refresh rate: {refresh_rate(device_info)}")
print(f"User's GPU: {gpuInfo(device_info)}")

def return_fps():
    return refresh_rate(device_info)