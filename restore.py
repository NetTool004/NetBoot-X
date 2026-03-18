# tweaks/restore.py

from __future__ import annotations
import subprocess
import os


def run_cmd(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    return output.strip() or f"Command executed. ExitCode={result.returncode}"


def restore_network_defaults() -> str:
    cmds = [
        'netsh int ip reset',
        'netsh winsock reset',
        'ipconfig /flushdns',
    ]
    return "\n\n".join(run_cmd(c) for c in cmds)


def restore_power_defaults() -> str:
    return run_cmd('powercfg -restoredefaultschemes')


def open_windows_recovery() -> str:
    os.system('start ms-settings:recovery')
    return "Opened Windows Recovery settings."