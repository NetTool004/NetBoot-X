import customtkinter as ctk


def build_system_page(parent, app):
    root = ctk.CTkFrame(parent, fg_color="#03163d", corner_radius=22)
    root.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

    title = ctk.CTkLabel(
        root,
        text=app.t("system_title"),
        font=ctk.CTkFont(size=24, weight="bold"),
        anchor="w"
    )
    title.pack(fill="x", padx=24, pady=(22, 6))

    desc = ctk.CTkLabel(
        root,
        text=app.t("system_desc"),
        font=ctk.CTkFont(size=15),
        text_color="#9cc9ff",
        anchor="w"
    )
    desc.pack(fill="x", padx=24, pady=(0, 18))

    box = ctk.CTkFrame(root, fg_color="#0a245a", corner_radius=18)
    box.pack(fill="x", padx=24, pady=10)

    labels = [app.t("sys_temp"), app.t("sys_visual"), app.t("sys_power")]
    for i, text in enumerate(labels):
        item = ctk.CTkLabel(box, text=f"• {text}", font=ctk.CTkFont(size=16), anchor="w")
        item.pack(fill="x", padx=18, pady=(14 if i == 0 else 4, 4))

    current = app.t("status_on") if app.app_state["system_enabled"] else app.t("status_off")
    status = ctk.CTkLabel(
        box,
        text=f"{app.t('system')}: {current}",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#79b8ff",
        anchor="w"
    )
    status.pack(fill="x", padx=18, pady=(10, 18))

    action_text = app.t("disable") if app.app_state["system_enabled"] else app.t("apply")
    action_btn = ctk.CTkButton(
        root,
        text=action_text,
        height=42,
        fg_color="#3c8fe6",
        hover_color="#4ea0f5",
        command=app.toggle_system
    )
    action_btn.pack(padx=24, pady=18, anchor="w")