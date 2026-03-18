# ui/restore_page.py

from __future__ import annotations
import customtkinter as ctk
from tweaks import restore


class RestorePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        title = ctk.CTkLabel(self, text="Restore / Recovery", font=ctk.CTkFont(size=30, weight="bold"))
        title.pack(anchor="w", padx=24, pady=(24, 10))

        card = ctk.CTkFrame(self, corner_radius=16)
        card.pack(fill="x", padx=18, pady=12)

        ctk.CTkLabel(card, text="Recovery Actions", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=18, pady=(16, 10))

        self._btn(card, "Restore Network Defaults", lambda: self.run_admin("Restore Network Defaults", restore.restore_network_defaults))
        self._btn(card, "Restore System Power Defaults", lambda: self.run_admin("Restore System Power Defaults", restore.restore_power_defaults))
        self._btn(card, "Open Windows Recovery", restore.open_windows_recovery)

        self.log = ctk.CTkTextbox(self, height=260)
        self.log.pack(fill="both", expand=True, padx=18, pady=(8, 18))
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