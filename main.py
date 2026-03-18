# main.py
# NetBoot X FINAL PACK
# - Auto-launch after installer (no 740)
# - AppData save (auto-create netbootx_state.json)
# - Admin-ready (elevate only when running protected tweaks)
# - Professional CTk layout
# - Full UI page wiring

from __future__ import annotations

import json
import os
import sys
import ctypes
import traceback
from pathlib import Path
from typing import Optional, Dict, Any

import customtkinter as ctk

from ui.dashboard import DashboardPage
from ui.net_page import NetPage
from ui.system_page import SystemPage
from ui.boot_page import BootPage
from ui.restore_page import RestorePage

APP_NAME = "NetBoot X"
APP_DIR_NAME = "NetBootX"
STATE_FILE_NAME = "netbootx_state.json"


# =========================================================
# PATH HELPERS
# =========================================================
def get_base_path() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


BASE_PATH = get_base_path()
ASSETS_DIR = BASE_PATH / "assets"
CONFIG_DIR = BASE_PATH / "config"

APPDATA_DIR = Path(os.getenv("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))) / APP_DIR_NAME
APPDATA_DIR.mkdir(parents=True, exist_ok=True)

STATE_PATH = APPDATA_DIR / STATE_FILE_NAME


def asset_path(*parts: str) -> Path:
    return ASSETS_DIR.joinpath(*parts)


def config_path(*parts: str) -> Path:
    return CONFIG_DIR.joinpath(*parts)


# =========================================================
# STATE
# =========================================================
DEFAULT_STATE: Dict[str, Any] = {
    "theme": "dark",
    "last_page": "dashboard",
    "window_width": 1240,
    "window_height": 780,
}


def ensure_state_file() -> None:
    if not STATE_PATH.exists():
        try:
            with open(STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_STATE, f, indent=2, ensure_ascii=False)
        except Exception:
            pass


def load_state() -> Dict[str, Any]:
    ensure_state_file()
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return DEFAULT_STATE.copy()
        merged = DEFAULT_STATE.copy()
        merged.update(data)
        return merged
    except Exception:
        return DEFAULT_STATE.copy()


def save_state(data: Dict[str, Any]) -> None:
    try:
        APPDATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# =========================================================
# ADMIN HELPERS
# =========================================================
def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin() -> bool:
    try:
        exe = sys.executable
        if getattr(sys, "frozen", False):
            params = ""
        else:
            script = str(Path(__file__).resolve())
            params = f'"{script}"'

        rc = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            exe,
            params,
            None,
            1
        )
        return rc > 32
    except Exception:
        return False


# =========================================================
# APP
# =========================================================
class NetBootXApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.state_data = load_state()

        ctk.set_appearance_mode(self.state_data.get("theme", "dark"))
        ctk.set_default_color_theme("blue")

        self.title(APP_NAME)
        self.geometry(f"{self.state_data.get('window_width', 1240)}x{self.state_data.get('window_height', 780)}")
        self.minsize(1120, 720)

        try:
            ico = asset_path("icon.ico")
            if ico.exists():
                self.iconbitmap(str(ico))
        except Exception:
            pass

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_rowconfigure(20, weight=1)

        # Content
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.pages: Dict[str, ctk.CTkFrame] = {}

        self._build_sidebar()
        self._create_pages()

        last_page = self.state_data.get("last_page", "dashboard")
        self.show_page(last_page if last_page in self.pages else "dashboard")

    def _build_sidebar(self) -> None:
        title = ctk.CTkLabel(
            self.sidebar,
            text="NETBOOT X",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(24, 6), sticky="w")

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Performance • Network • Recovery",
            font=ctk.CTkFont(size=12)
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 18), sticky="w")

        self.btn_dashboard = self._nav_btn("Dashboard", 2, lambda: self.show_page("dashboard"))
        self.btn_network = self._nav_btn("Network Tweaks", 3, lambda: self.show_page("network"))
        self.btn_system = self._nav_btn("System Tweaks", 4, lambda: self.show_page("system"))
        self.btn_boot = self._nav_btn("Boot Tweaks", 5, lambda: self.show_page("boot"))
        self.btn_restore = self._nav_btn("Restore", 6, lambda: self.show_page("restore"))

        self.admin_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Admin: {'YES' if is_admin() else 'NO'}",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.admin_label.grid(row=21, column=0, padx=20, pady=(8, 4), sticky="sw")

        self.theme_btn = ctk.CTkButton(
            self.sidebar,
            text="Toggle Theme",
            height=40,
            command=self.toggle_theme
        )
        self.theme_btn.grid(row=22, column=0, padx=18, pady=(8, 20), sticky="ew")

    def _nav_btn(self, text: str, row: int, command):
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=42,
            anchor="w",
            command=command
        )
        btn.grid(row=row, column=0, padx=16, pady=6, sticky="ew")
        return btn

    def _create_pages(self) -> None:
        self.pages["dashboard"] = DashboardPage(self.content, self)
        self.pages["network"] = NetPage(self.content, self)
        self.pages["system"] = SystemPage(self.content, self)
        self.pages["boot"] = BootPage(self.content, self)
        self.pages["restore"] = RestorePage(self.content, self)

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")
            page.grid_remove()

    def show_page(self, page_name: str) -> None:
        for name, page in self.pages.items():
            if name == page_name:
                page.grid()
                if hasattr(page, "on_show"):
                    try:
                        page.on_show()
                    except Exception:
                        pass
            else:
                page.grid_remove()

        self.state_data["last_page"] = page_name

    def toggle_theme(self) -> None:
        current = self.state_data.get("theme", "dark")
        new_theme = "light" if current == "dark" else "dark"
        ctk.set_appearance_mode(new_theme)
        self.state_data["theme"] = new_theme
        save_state(self.state_data)

    def request_admin_and_run(self, action_name: str, func, *args, **kwargs):
        """
        If app already elevated -> run immediately
        Else ask user to relaunch whole app as admin (avoids installer auto-launch 740)
        """
        if is_admin():
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.show_error(action_name, str(e))
                return None

        dialog = ctk.CTkToplevel(self)
        dialog.title("Administrator Required")
        dialog.geometry("460x230")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=f'"{action_name}" requires Administrator privileges.\n\n'
                 f'Click "Relaunch as Admin" to restart NetBoot X with elevation.',
            justify="left",
            wraplength=400
        ).pack(padx=20, pady=(24, 14), fill="x")

        def do_relaunch():
            dialog.destroy()
            ok = relaunch_as_admin()
            if ok:
                self.after(250, self.destroy)
            else:
                self.show_error("Elevation Failed", "Unable to relaunch as administrator.")

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkButton(btn_frame, text="Relaunch as Admin", command=do_relaunch).pack(
            side="left", expand=True, fill="x", padx=(0, 6)
        )
        ctk.CTkButton(btn_frame, text="Cancel", command=dialog.destroy).pack(
            side="left", expand=True, fill="x", padx=(6, 0)
        )

        dialog.wait_window()

    def show_message(self, title: str, message: str) -> None:
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("560x320")
        win.grab_set()

        ctk.CTkLabel(
            win,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(padx=20, pady=(18, 8), anchor="w")

        box = ctk.CTkTextbox(win, wrap="word")
        box.pack(padx=20, pady=(0, 16), fill="both", expand=True)
        box.insert("1.0", message)
        box.configure(state="disabled")

        ctk.CTkButton(win, text="OK", command=win.destroy).pack(padx=20, pady=(0, 18))

    def show_error(self, title: str, message: str) -> None:
        self.show_message(title, message)

    def on_close(self) -> None:
        try:
            self.state_data["window_width"] = max(self.winfo_width(), 1120)
            self.state_data["window_height"] = max(self.winfo_height(), 720)
            save_state(self.state_data)
        except Exception:
            pass
        self.destroy()


def main():
    ensure_state_file()
    app = NetBootXApp()
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        err = traceback.format_exc()
        try:
            ctypes.windll.user32.MessageBoxW(
                0,
                f"NetBoot X crashed:\n\n{err}",
                "NetBoot X Error",
                0x10
            )
        except Exception:
            print(err)