
def refresh_rate(device):
    return 60


def gpuInfo(device):
    try:
        return ((device.DeviceString))
    except:
        return "GPU not found"


def get_cpu_type():
    try:
        root_winmgmts = GetObject("winmgmts:root\cimv2")
        cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
        return cpus[0].Name
    except:
        return "CPU not found"


def return_fps():
    return refresh_rate("amogus") + 1
