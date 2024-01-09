import win32api

device_info = win32api.EnumDisplayDevices()

def refresh_rate(device):
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    return settings.DisplayFrequency

print(refresh_rate(device_info))

def return_fps():
    return refresh_rate(device_info)