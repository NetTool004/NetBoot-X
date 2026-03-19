# tweaks/system_tweaks.py

from __future__ import annotations
import subprocess
import tempfile
import shutil
from pathlib import Path


def run_cmd(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    return output.strip() or f"Command executed. ExitCode={result.returncode}"


def disable_hibernation() -> str:
    return run_cmd('powercfg -h off')


def enable_ultimate_performance() -> str:
    cmds = [
        'powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61',
        'powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61',
    ]
    return "\n\n".join(run_cmd(c) for c in cmds)


def clear_temp_files() -> str:
    temp_dir = Path(tempfile.gettempdir())
    deleted = 0
    failed = 0

    for item in temp_dir.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink(missing_ok=True)
                deleted += 1
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
                deleted += 1
        except Exception:
            failed += 1

    return f"Temp cleanup completed.\nDeleted items: {deleted}\nFailed items: {failed}"


def create_restore_point() -> str:
    cmd = (
        'powershell -ExecutionPolicy Bypass -Command '
        '"Checkpoint-Computer -Description \\"NetBootX Restore Point\\" -RestorePointType \\"MODIFY_SETTINGS\\""'
    )
    return run_cmd(cmd)


def run_sfc_scan() -> str:
    return run_cmd('sfc /scannow')