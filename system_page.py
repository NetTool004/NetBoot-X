# ui/system_page.py

from __future__ import annotations
import customtkinter as ctk
from tweaks import system_tweaks


class SystemPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_columnconfigure((0, 1), weight=1)

        title = ctk.CTkLabel(self, text="System Tweaks", font=ctk.CTkFont(size=30, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, padx=24, pady=(24, 10), sticky="w")

        left = ctk.CTkFrame(self, corner_radius=16)
        left.grid(row=1, column=0, padx=18, pady=12, sticky="nsew")

        right = ctk.CTkFrame(self, corner_radius=16)
        right.grid(row=1, column=1, padx=18, pady=12, sticky="nsew")

        ctk.CTkLabel(left, text="Performance", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=18, pady=(16, 10))
        self._btn(left, "Disable Hibernation", lambda: self.run_admin("Disable Hibernation", system_tweaks.disable_hibernation))
        self._btn(left, "Ultimate Performance Plan", lambda: self.run_admin("Ultimate Performance Plan", system_tweaks.enable_ultimate_performance))
        self._btn(left, "Clear Temp Files", self.run_user_clear_temp)

        ctk.CTkLabel(right, text="System Safety", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=18, pady=(16, 10))
        self._btn(right, "Create Restore Point (PowerShell)", lambda: self.run_admin("Create Restore Point", system_tweaks.create_restore_point))
        self._btn(right, "System File Check (SFC)", lambda: self.run_admin("System File Check (SFC)", system_tweaks.run_sfc_scan))

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

    def run_user_clear_temp(self):
        try:
            result = system_tweaks.clear_temp_files()
            self.write_log(f"[OK] Clear Temp Files\n{result}")
            self.app.show_message("Clear Temp Files", str(result))
        except Exception as e:
            self.app.show_error("Clear Temp Files", str(e))

    def write_log(self, text: str):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n\n")
        self.log.see("end")
        self.log.configure(state="disabled")