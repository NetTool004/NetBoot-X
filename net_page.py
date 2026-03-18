# ui/net_page.py

from __future__ import annotations
import customtkinter as ctk
from tweaks import net_tweaks


class NetPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_columnconfigure((0, 1), weight=1)

        title = ctk.CTkLabel(self, text="Network Tweaks", font=ctk.CTkFont(size=30, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, padx=24, pady=(24, 10), sticky="w")

        left = ctk.CTkFrame(self, corner_radius=16)
        left.grid(row=1, column=0, padx=18, pady=12, sticky="nsew")

        right = ctk.CTkFrame(self, corner_radius=16)
        right.grid(row=1, column=1, padx=18, pady=12, sticky="nsew")

        ctk.CTkLabel(left, text="Performance Tweaks", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=18, pady=(16, 10))

        self._btn(left, "Net_Tweak_FULL_AX210_AUTO", lambda: self.run_admin("Net_Tweak_FULL_AX210_AUTO", net_tweaks.net_tweak_full_ax210_auto))
        self._btn(left, "AX210_Gaming_Tweak", lambda: self.run_admin("AX210_Gaming_Tweak", net_tweaks.ax210_gaming_tweak))
        self._btn(left, "AX210_WIFI_REFRESH", lambda: self.run_admin("AX210_WIFI_REFRESH", net_tweaks.ax210_wifi_refresh))
        self._btn(left, "Set DNS Cloudflare", lambda: self.run_admin("Set DNS Cloudflare", net_tweaks.set_dns_cloudflare))
        self._btn(left, "Flush DNS + Winsock Reset", lambda: self.run_admin("Flush DNS + Winsock Reset", net_tweaks.flush_dns_and_reset))
        self._btn(left, "Disable TCP AutoTuning", lambda: self.run_admin("Disable TCP AutoTuning", net_tweaks.disable_tcp_autotuning))
        self._btn(left, "Enable TCP AutoTuning", lambda: self.run_admin("Enable TCP AutoTuning", net_tweaks.enable_tcp_autotuning))

        ctk.CTkLabel(right, text="Restore / Safe", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=18, pady=(16, 10))

        self._btn(right, "AX210_RESTORE_DEFAULT", lambda: self.run_admin("AX210_RESTORE_DEFAULT", net_tweaks.ax210_restore_default))
        self._btn(right, "Restore DNS Automatic", lambda: self.run_admin("Restore DNS Automatic", net_tweaks.restore_dns_automatic))

        self.log = ctk.CTkTextbox(self, height=220)
        self.log.grid(row=2, column=0, columnspan=2, padx=18, pady=(8, 18), sticky="ew")
        self.log.insert("1.0", "Ready.\n")
        self.log.configure(state="disabled")

    def _btn(self, parent, text, cmd):
        ctk.CTkButton(parent, text=text, height=42, command=cmd).pack(fill="x", padx=18, pady=8)

    def run_admin(self, name, func):
        def wrapped():
            result = func()
            self.write_log(f"[OK] {name}\n{result}")
            self.app.show_message(name, str(result))

        self.app.request_admin_and_run(name, wrapped)

    def write_log(self, text: str):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n\n")
        self.log.see("end")
        self.log.configure(state="disabled")