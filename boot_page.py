# ui/boot_page.py

from __future__ import annotations
import customtkinter as ctk
from tweaks import boot_tweaks


class BootPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_columnconfigure((0, 1), weight=1)

        title = ctk.CTkLabel(self, text="Boot Tweaks", font=ctk.CTkFont(size=30, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, padx=24, pady=(24, 10), sticky="w")

        left = ctk.CTkFrame(self, corner_radius=16)
        left.grid(row=1, column=0, padx=18, pady=12, sticky="nsew")

        right = ctk.CTkFrame(self, corner_radius=16)
        right.grid(row=1, column=1, padx=18, pady=12, sticky="nsew")

        ctk.CTkLabel(left, text="Boot Optimization", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=18, pady=(16, 10))
        self._btn(left, "Disable Boot Menu Timeout", lambda: self.run_admin("Disable Boot Menu Timeout", boot_tweaks.disable_boot_menu_timeout))
        self._btn(left, "Enable Fast Boot (BCD)", lambda: self.run_admin("Enable Fast Boot (BCD)", boot_tweaks.enable_fast_boot_bcd))
        self._btn(left, "Set Timeout 3 sec", lambda: self.run_admin("Set Timeout 3 sec", boot_tweaks.set_boot_timeout_3))

        ctk.CTkLabel(right, text="Restore Boot Defaults", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=18, pady=(16, 10))
        self._btn(right, "Restore Default Boot Timeout", lambda: self.run_admin("Restore Default Boot Timeout", boot_tweaks.restore_default_boot_timeout))

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