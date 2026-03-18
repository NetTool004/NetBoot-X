# ui/dashboard.py

from __future__ import annotations
import customtkinter as ctk
import platform
import socket
import psutil


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=24, pady=(24, 10), sticky="w")

        self.sys_card = self._make_card("System Overview", 1, 0)
        self.net_card = self._make_card("Network Overview", 1, 1)
        self.quick_card = self._make_card("Quick Actions", 2, 0)
        self.info_card = self._make_card("Tips", 2, 1)

        self._fill_system_card()
        self._fill_network_card()
        self._fill_quick_card()
        self._fill_info_card()

    def _make_card(self, title: str, row: int, col: int):
        card = ctk.CTkFrame(self, corner_radius=16)
        card.grid(row=row, column=col, padx=18, pady=12, sticky="nsew")

        label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(anchor="w", padx=18, pady=(16, 10))
        return card

    def _fill_system_card(self):
        try:
            cpu = platform.processor() or "Unknown CPU"
            os_name = f"{platform.system()} {platform.release()}"
            ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)

            lines = [
                f"OS: {os_name}",
                f"CPU: {cpu}",
                f"RAM: {ram_gb} GB",
                f"Admin: {'YES' if self.app.admin_label.cget('text').endswith('YES') else 'NO'}",
            ]
        except Exception:
            lines = ["Unable to read system information."]

        for line in lines:
            ctk.CTkLabel(self.sys_card, text=line, anchor="w").pack(anchor="w", padx=18, pady=4)

    def _fill_network_card(self):
        try:
            host = socket.gethostname()
            ip = socket.gethostbyname(host)
            stats = psutil.net_if_stats()
            up_ifaces = [name for name, s in stats.items() if s.isup]
            iface_text = ", ".join(up_ifaces[:4]) if up_ifaces else "None"
            lines = [
                f"Hostname: {host}",
                f"IPv4: {ip}",
                f"Active adapters: {iface_text}",
            ]
        except Exception:
            lines = ["Unable to read network information."]

        for line in lines:
            ctk.CTkLabel(self.net_card, text=line, anchor="w").pack(anchor="w", padx=18, pady=4)

    def _fill_quick_card(self):
        ctk.CTkButton(
            self.quick_card,
            text="Open Network Tweaks",
            command=lambda: self.app.show_page("network")
        ).pack(fill="x", padx=18, pady=8)

        ctk.CTkButton(
            self.quick_card,
            text="Open System Tweaks",
            command=lambda: self.app.show_page("system")
        ).pack(fill="x", padx=18, pady=8)

        ctk.CTkButton(
            self.quick_card,
            text="Open Boot Tweaks",
            command=lambda: self.app.show_page("boot")
        ).pack(fill="x", padx=18, pady=8)

        ctk.CTkButton(
            self.quick_card,
            text="Open Restore",
            command=lambda: self.app.show_page("restore")
        ).pack(fill="x", padx=18, pady=(8, 16))

    def _fill_info_card(self):
        tips = [
            "• Run tweaks as Administrator for full effect.",
            "• Network tweaks may reset adapter / TCP stack.",
            "• Use Restore page before testing aggressive tweaks.",
            "• App settings auto-save in AppData.",
        ]
        for tip in tips:
            ctk.CTkLabel(self.info_card, text=tip, justify="left", anchor="w").pack(anchor="w", padx=18, pady=5)