import subprocess

CREATE_NO_WINDOW = 0x08000000

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
        ok = result.returncode == 0
        output = (result.stdout or "") + (result.stderr or "")
        return ok, output.strip() or "Done"
    except Exception as e:
        return False, str(e)

def set_dns_cloudflare():
    ok1, out1 = run_cmd(["netsh", "interface", "ip", "set", "dns", "name=Ethernet", "static", "1.1.1.1"])
    ok2, out2 = run_cmd(["netsh", "interface", "ip", "add", "dns", "name=Ethernet", "1.0.0.1", "index=2"])
    ok3, out3 = run_cmd(["netsh", "interface", "ip", "set", "dns", "name=Wi-Fi", "static", "1.1.1.1"])
    ok4, out4 = run_cmd(["netsh", "interface", "ip", "add", "dns", "name=Wi-Fi", "1.0.0.1", "index=2"])
    return (ok1 or ok3), out1 or out3 or out2 or out4

def reset_dns_dhcp():
    ok1, out1 = run_cmd(["netsh", "interface", "ip", "set", "dns", "name=Ethernet", "dhcp"])
    ok2, out2 = run_cmd(["netsh", "interface", "ip", "set", "dns", "name=Wi-Fi", "dhcp"])
    return (ok1 or ok2), out1 or out2

def flush_dns():
    return run_cmd(["ipconfig", "/flushdns"])

def reset_network():
    ok1, out1 = run_cmd(["netsh", "winsock", "reset"])
    ok2, out2 = run_cmd(["netsh", "int", "ip", "reset"])
    return (ok1 and ok2), (out1 + " | " + out2)