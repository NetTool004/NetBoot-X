from tweaks.net_tweaks import run_cmd

def enable_fast_startup():
    return run_cmd(["reg", "add", r"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power", "/v", "HiberbootEnabled", "/t", "REG_DWORD", "/d", "1", "/f"])

def disable_fast_startup():
    return run_cmd(["reg", "add", r"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power", "/v", "HiberbootEnabled", "/t", "REG_DWORD", "/d", "0", "/f"])

def enable_hibernation():
    return run_cmd(["powercfg", "/hibernate", "on"])

def disable_hibernation():
    return run_cmd(["powercfg", "/hibernate", "off"])