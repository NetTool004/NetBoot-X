# tweaks/boot_tweaks.py

from __future__ import annotations
import subprocess


def run_cmd(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    return output.strip() or f"Command executed. ExitCode={result.returncode}"


def disable_boot_menu_timeout() -> str:
    return run_cmd('bcdedit /timeout 0')


def enable_fast_boot_bcd() -> str:
    return run_cmd('bcdedit /set {current} bootmenupolicy standard')


def set_boot_timeout_3() -> str:
    return run_cmd('bcdedit /timeout 3')


def restore_default_boot_timeout() -> str:
    return run_cmd('bcdedit /timeout 30')