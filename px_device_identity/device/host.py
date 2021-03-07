import platform
import psutil

def system_information():
    uname = platform.uname()
    memory = psutil.virtual_memory()[0]
    return {
        'operating_system': uname.system,
        'operating_system_release': uname.release,
        'system_architecture': uname.machine,
        'system_memory': memory
    }
