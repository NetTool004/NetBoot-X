# tweaks/net_tweaks.py

from __future__ import annotations
import subprocess


def run_cmd(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    return output.strip() or f"Command executed. ExitCode={result.returncode}"


def net_tweak_full_ax210_auto() -> str:
    cmds = [
        'netsh int tcp set global autotuninglevel=normal',
        'netsh int tcp set global rss=enabled',
        'netsh int tcp set global chimney=enabled',
        'ipconfig /flushdns',
    ]
    return "\n\n".join(run_cmd(c) for c in cmds)


def ax210_gaming_tweak() -> str:
    cmds = [
        'netsh int tcp set global ecncapability=disabled',
        'netsh int tcp set global timestamps=disabled',
        'netsh int tcp set global rss=enabled',
    ]
    return "\n\n".join(run_cmd(c) for c in cmds)


def ax210_wifi_refresh() -> str:
    cmds = [
        'ipconfig /release',
        'ipconfig /renew',
        'ipconfig /flushdns',
    ]
    return "\n\n".join(run_cmd(c) for c in cmds)


def ax210_restore_default() -> str:
    cmds = [
        'netsh int ip reset',
        'netsh winsock reset',
        'netsh int tcp set global autotuninglevel=normal',
    ]
    return "\n\n".join(run_cmd(c) for c in cmds)


def set_dns_cloudflare() -> str:
    # Generic safe reset; manual adapter targeting can be added later
    return (
        "Open adapter IPv4 manually and set:\n"
        "Preferred DNS: 1.1.1.1\n"
        "Alternate DNS: 1.0.0.1\n\n"
        "Tip: This build keeps it safe because adapter names vary per machine."
    )


def restore_dns_automatic() -> str:
    return "Set your adapter IPv4 DNS back to Automatic (DHCP)."


def flush_dns_and_reset() -> str:
    cmds = [
        'ipconfig /flushdns',
        'netsh winsock reset',
    ]
    return "\n\n".join(run_cmd(c) for c in cmds)


def disable_tcp_autotuning() -> str:
    return run_cmd('netsh int tcp set global autotuninglevel=disabled')


def enable_tcp_autotuning() -> str:
    return run_cmd('netsh int tcp set global autotuninglevel=normal')