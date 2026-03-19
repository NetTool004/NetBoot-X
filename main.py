import os
import json
import ctypes
import customtkinter as ctk

from ui.dashboard import build_dashboard
from ui.net_page import build_net_page
from ui.boot_page import build_boot_page
from ui.system_page import build_system_page
from ui.restore_page import build_restore_page

# ---------------------------
# CONFIG
# ---------------------------
APP_NAME = "NetBoot X"
STATE_FILE = "netbootx_state.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------------------
# TRANSLATIONS
# ---------------------------
TRANSLATIONS = {
    "TH": {
        "title": "NetBoot X",
        "subtitle": "Safe Tweaks Only",
        "dashboard": "แดชบอร์ด",
        "net": "Net Boost",
        "boot": "Boot Boost",
        "system": "System Boost",
        "restore": "Restore",
        "language_label": "ภาษา / TH-EN-CH",
        "admin_status": "สิทธิ์แอดมิน",
        "admin_yes": "มี",
        "admin_no": "ไม่มี",
        "restore_system": "รีสตาร์ทเพื่อให้บางการตั้งค่ามีผล",
        "lang_code": "TH",

        # Dashboard
        "dashboard_title": "แดชบอร์ด",
        "dashboard_main": "NetBoot X - ตัวช่วยเร่งระบบแบบปลอดภัย",
        "dashboard_sub": "สำหรับ Network / Boot / System",
        "system_ready": "พร้อมใช้งาน",
        "system_status": "สถานะระบบ",

        # Cards
        "status_on": "เปิด",
        "status_off": "ปิด",

        # Log
        "log_started": "NetBoot X เริ่มทำงานแล้ว",

        # Net Page
        "net_title": "Net Boost",
        "net_desc": "ปรับแต่ง Network แบบปลอดภัย เพื่อให้ตอบสนองดีขึ้น",
        "net_dns": "ใช้ DNS เร็ว (Cloudflare)",
        "net_tcp": "TCP Optimized",
        "net_flush": "ล้าง DNS Cache",
        "apply": "เปิดใช้งาน",
        "disable": "ปิดใช้งาน",

        # Boot Page
        "boot_title": "Boot Boost",
        "boot_desc": "ปรับแต่งการบูตแบบปลอดภัย เพื่อให้เปิดเครื่องไวขึ้น",
        "boot_fast": "Fast Boot Profile",
        "boot_delay": "ลด Boot Delay",
        "boot_timeout": "ลด Timeout เมนูบูต",

        # System Page
        "system_title": "System Boost",
        "system_desc": "ปรับแต่งระบบแบบปลอดภัย เพื่อให้ลื่นและตอบสนองไวขึ้น",
        "sys_temp": "ล้างไฟล์ Temp",
        "sys_visual": "ปรับ Visual Performance",
        "sys_power": "High Performance Mode",

        # Restore Page
        "restore_title": "Restore",
        "restore_desc": "คืนค่าการปรับแต่งกลับสู่ค่าเริ่มต้นอย่างปลอดภัย",
        "restore_all": "คืนค่าทั้งหมด",
        "restore_note": "เหมาะสำหรับย้อนกลับการปรับแต่งทั้งหมด",

        # Footer
        "footer_admin": "สิทธิ์แอดมิน:",
        "footer_restart": "รีบูตให้มีผลบางระบบ",
    },

    "EN": {
        "title": "NetBoot X",
        "subtitle": "Safe Tweaks Only",
        "dashboard": "Dashboard",
        "net": "Net Boost",
        "boot": "Boot Boost",
        "system": "System Boost",
        "restore": "Restore",
        "language_label": "Language / TH-EN-CH",
        "admin_status": "Admin Rights",
        "admin_yes": "Yes",
        "admin_no": "No",
        "restore_system": "Restart required for some tweaks",
        "lang_code": "EN",

        "dashboard_title": "Dashboard",
        "dashboard_main": "NetBoot X - Safe Windows Optimizer",
        "dashboard_sub": "For Network / Boot / System",
        "system_ready": "Ready",
        "system_status": "System Status",

        "status_on": "ON",
        "status_off": "OFF",

        "log_started": "NetBoot X started",

        "net_title": "Net Boost",
        "net_desc": "Safe network tweaks for better responsiveness",
        "net_dns": "Fast DNS (Cloudflare)",
        "net_tcp": "TCP Optimized",
        "net_flush": "Flush DNS Cache",
        "apply": "Enable",
        "disable": "Disable",

        "boot_title": "Boot Boost",
        "boot_desc": "Safe boot tweaks for faster startup",
        "boot_fast": "Fast Boot Profile",
        "boot_delay": "Reduce Boot Delay",
        "boot_timeout": "Reduce Boot Menu Timeout",

        "system_title": "System Boost",
        "system_desc": "Safe system tweaks for smoother performance",
        "sys_temp": "Clean Temp Files",
        "sys_visual": "Optimize Visual Performance",
        "sys_power": "High Performance Mode",

        "restore_title": "Restore",
        "restore_desc": "Safely restore all tweaks to default",
        "restore_all": "Restore All",
        "restore_note": "Recommended to undo all changes",

        "footer_admin": "Admin Rights:",
        "footer_restart": "Restart required for some tweaks",
    },

    "CH": {
        "title": "NetBoot X",
        "subtitle": "仅安全优化",
        "dashboard": "仪表板",
        "net": "网络加速",
        "boot": "启动加速",
        "system": "系统加速",
        "restore": "恢复",
        "language_label": "语言 / TH-EN-CH",
        "admin_status": "管理员权限",
        "admin_yes": "有",
        "admin_no": "无",
        "restore_system": "部分优化需要重启后生效",
        "lang_code": "CH",

        "dashboard_title": "仪表板",
        "dashboard_main": "NetBoot X - 安全系统优化工具",
        "dashboard_sub": "适用于 Network / Boot / System",
        "system_ready": "可用",
        "system_status": "系统状态",

        "status_on": "开",
        "status_off": "关",

        "log_started": "NetBoot X 已启动",

        "net_title": "网络加速",
        "net_desc": "安全优化网络响应速度",
        "net_dns": "快速 DNS (Cloudflare)",
        "net_tcp": "TCP 优化",
        "net_flush": "清除 DNS 缓存",
        "apply": "启用",
        "disable": "关闭",

        "boot_title": "启动加速",
        "boot_desc": "安全优化启动速度",
        "boot_fast": "快速启动配置",
        "boot_delay": "减少启动延迟",
        "boot_timeout": "减少启动菜单等待时间",

        "system_title": "系统加速",
        "system_desc": "安全优化系统流畅度",
        "sys_temp": "清理临时文件",
        "sys_visual": "优化视觉效果",
        "sys_power": "高性能模式",

        "restore_title": "恢复",
        "restore_desc": "安全恢复所有优化到默认值",
        "restore_all": "恢复全部",
        "restore_note": "建议用于撤销所有优化",

        "footer_admin": "管理员权限:",
        "footer_restart": "部分优化需要重启",
    }
}


# ---------------------------
# HELPERS
# ---------------------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def load_app_state():
    default_state = {
        "language": "TH",
        "net_enabled": False,
        "boot_enabled": False,
        "system_enabled": False
    }

    if not os.path.exists(STATE_FILE):
        return default_state

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key in default_state:
            if key not in data:
                data[key] = default_state[key]
        return data
    except:
        return default_state


def save_app_state(data):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass


# ---------------------------
# APP
# ---------------------------
class NetBootXApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # IMPORTANT: DON'T USE self.state !!!
        self.app_state = load_app_state()

        self.title(APP_NAME)
        self.geometry("1280x820")
        self.minsize(1100, 700)

        self.translations = TRANSLATIONS
        self.current_lang = self.app_state.get("language", "TH")

        self.admin_mode = bool(is_admin())

        self.sidebar = None
        self.content_frame = None
        self.header_label = None
        self.page_container = None
        self.log_box = None
        self.lang_menu = None

        self.nav_buttons = {}
        self.current_page = "dashboard"

        self.build_ui()
        self.show_page("dashboard")
        self.log(self.t("log_started"))

    def t(self, key):
        return self.translations.get(self.current_lang, self.translations["TH"]).get(key, key)

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=245, corner_radius=0, fg_color="#031a44")
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        self.sidebar.grid_rowconfigure(9, weight=1)

        self.app_title = ctk.CTkLabel(
            self.sidebar,
            text=self.t("title"),
            font=ctk.CTkFont(size=34, weight="bold"),
            anchor="w"
        )
        self.app_title.grid(row=0, column=0, padx=22, pady=(20, 6), sticky="ew")

        self.app_subtitle = ctk.CTkLabel(
            self.sidebar,
            text=self.t("subtitle"),
            font=ctk.CTkFont(size=22),
            text_color="#cce2ff",
            anchor="w"
        )
        self.app_subtitle.grid(row=1, column=0, padx=22, pady=(0, 22), sticky="ew")

        # Nav buttons
        nav_items = [
            ("dashboard", self.t("dashboard")),
            ("net", self.t("net")),
            ("boot", self.t("boot")),
            ("system", self.t("system")),
            ("restore", self.t("restore")),
        ]

        for i, (page_key, label) in enumerate(nav_items, start=2):
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                height=38,
                corner_radius=8,
                fg_color="#3c8fe6" if page_key == "dashboard" else "#337bc5",
                hover_color="#4ea0f5",
                command=lambda p=page_key: self.show_page(p)
            )
            btn.grid(row=i, column=0, padx=18, pady=7, sticky="ew")
            self.nav_buttons[page_key] = btn

        # Language label
        self.lang_label = ctk.CTkLabel(
            self.sidebar,
            text=self.t("language_label"),
            anchor="w"
        )
        self.lang_label.grid(row=7, column=0, padx=22, pady=(28, 8), sticky="ew")

        self.lang_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["TH", "EN", "CH"],
            command=self.change_language,
            height=32
        )
        self.lang_menu.set(self.current_lang)
        self.lang_menu.grid(row=8, column=0, padx=18, pady=(0, 18), sticky="ew")

        # Bottom info
        self.admin_label = ctk.CTkLabel(
            self.sidebar,
            text=f"{self.t('admin_status')}: {self.t('admin_yes') if self.admin_mode else self.t('admin_no')}",
            anchor="w"
        )
        self.admin_label.grid(row=10, column=0, padx=22, pady=(0, 8), sticky="ew")

        self.restart_hint = ctk.CTkButton(
            self.sidebar,
            text=self.t("restore_system"),
            height=34,
            fg_color="#337bc5",
            hover_color="#4ea0f5"
        )
        self.restart_hint.grid(row=11, column=0, padx=18, pady=(0, 20), sticky="ew")

        # Main area
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#02122f")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)

        # Header bar
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="#071d4a", corner_radius=18)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 12))

        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text=self.t("dashboard"),
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        self.header_label.pack(fill="x", padx=20, pady=16)

        # Page container
        self.page_container = ctk.CTkFrame(self.content_frame, fg_color="#02122f", corner_radius=0)
        self.page_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=0)
        self.page_container.grid_columnconfigure(0, weight=1)
        self.page_container.grid_rowconfigure(0, weight=1)

        # Log area
        self.log_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a1a", corner_radius=18)
        self.log_frame.grid(row=2, column=0, sticky="ew", padx=18, pady=(12, 18))

        self.log_box = ctk.CTkTextbox(self.log_frame, height=170, corner_radius=12)
        self.log_box.pack(fill="both", expand=True, padx=14, pady=14)
        self.log_box.configure(state="disabled")

    def clear_page(self):
        for widget in self.page_container.winfo_children():
            widget.destroy()

    def show_page(self, page_name):
        self.current_page = page_name
        self.clear_page()

        # update nav colors
        for key, btn in self.nav_buttons.items():
            btn.configure(fg_color="#3c8fe6" if key == page_name else "#337bc5")

        if page_name == "dashboard":
            self.header_label.configure(text=self.t("dashboard"))
            build_dashboard(self.page_container, self)
        elif page_name == "net":
            self.header_label.configure(text=self.t("net"))
            build_net_page(self.page_container, self)
        elif page_name == "boot":
            self.header_label.configure(text=self.t("boot"))
            build_boot_page(self.page_container, self)
        elif page_name == "system":
            self.header_label.configure(text=self.t("system"))
            build_system_page(self.page_container, self)
        elif page_name == "restore":
            self.header_label.configure(text=self.t("restore"))
            build_restore_page(self.page_container, self)

    def change_language(self, new_lang):
        self.current_lang = new_lang
        self.app_state["language"] = new_lang
        save_app_state(self.app_state)

        # Rebuild full UI
        for widget in self.winfo_children():
            widget.destroy()

        self.nav_buttons = {}
        self.build_ui()
        self.show_page(self.current_page)
        self.log(self.t("log_started"))

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    # Toggle actions
    def toggle_net(self):
        self.app_state["net_enabled"] = not self.app_state["net_enabled"]
        save_app_state(self.app_state)
        status = self.t("status_on") if self.app_state["net_enabled"] else self.t("status_off")
        self.log(f"[NET] {status}")
        self.show_page("net")

    def toggle_boot(self):
        self.app_state["boot_enabled"] = not self.app_state["boot_enabled"]
        save_app_state(self.app_state)
        status = self.t("status_on") if self.app_state["boot_enabled"] else self.t("status_off")
        self.log(f"[BOOT] {status}")
        self.show_page("boot")

    def toggle_system(self):
        self.app_state["system_enabled"] = not self.app_state["system_enabled"]
        save_app_state(self.app_state)
        status = self.t("status_on") if self.app_state["system_enabled"] else self.t("status_off")
        self.log(f"[SYSTEM] {status}")
        self.show_page("system")

    def restore_all(self):
        self.app_state["net_enabled"] = False
        self.app_state["boot_enabled"] = False
        self.app_state["system_enabled"] = False
        save_app_state(self.app_state)
        self.log("[RESTORE] All tweaks restored")
        self.show_page("restore")


if __name__ == "__main__":
    app = NetBootXApp()
    app.mainloop()