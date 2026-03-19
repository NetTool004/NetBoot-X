import customtkinter as ctk


def create_status_card(parent, title, status):
    card = ctk.CTkFrame(parent, fg_color="#0a245a", corner_radius=18)
    card.grid_columnconfigure(0, weight=1)

    title_label = ctk.CTkLabel(
        card,
        text=title,
        font=ctk.CTkFont(size=18, weight="bold"),
        anchor="w"
    )
    title_label.grid(row=0, column=0, padx=18, pady=(16, 8), sticky="ew")

    status_label = ctk.CTkLabel(
        card,
        text=status,
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color="#79b8ff",
        anchor="w"
    )
    status_label.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="ew")

    return card


def build_dashboard(parent, app):
    root = ctk.CTkFrame(parent, fg_color="#03163d", corner_radius=22)
    root.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

    root.grid_columnconfigure((0, 1), weight=1)

    # Title section
    title = ctk.CTkLabel(
        root,
        text=app.t("dashboard_main"),
        font=ctk.CTkFont(size=24, weight="bold"),
        anchor="w",
        justify="left"
    )
    title.grid(row=0, column=0, columnspan=2, padx=24, pady=(22, 4), sticky="ew")

    subtitle = ctk.CTkLabel(
        root,
        text=app.t("dashboard_sub"),
        font=ctk.CTkFont(size=15),
        text_color="#9cc9ff",
        anchor="w",
        justify="left"
    )
    subtitle.grid(row=1, column=0, columnspan=2, padx=24, pady=(0, 8), sticky="ew")

    admin_text = f"{app.t('admin_status')}: {app.t('admin_yes') if app.admin_mode else app.t('admin_no')}"
    admin_label = ctk.CTkLabel(
        root,
        text=admin_text,
        font=ctk.CTkFont(size=14),
        anchor="w"
    )
    admin_label.grid(row=2, column=0, padx=24, pady=(0, 16), sticky="w")

    lang_label = ctk.CTkLabel(
        root,
        text=f"{app.t('language_label').split('/')[0].strip()}: {app.t('lang_code')}",
        font=ctk.CTkFont(size=14),
        anchor="e"
    )
    lang_label.grid(row=2, column=1, padx=24, pady=(0, 16), sticky="e")

    # Cards
    net_status = app.t("status_on") if app.app_state["net_enabled"] else app.t("status_off")
    boot_status = app.t("status_on") if app.app_state["boot_enabled"] else app.t("status_off")
    sys_status = app.t("status_on") if app.app_state["system_enabled"] else app.t("status_off")

    card1 = create_status_card(root, app.t("net"), net_status)
    card1.grid(row=3, column=0, padx=(24, 12), pady=12, sticky="nsew")

    card2 = create_status_card(root, app.t("boot"), boot_status)
    card2.grid(row=3, column=1, padx=(12, 24), pady=12, sticky="nsew")

    card3 = create_status_card(root, app.t("system"), sys_status)
    card3.grid(row=4, column=0, padx=(24, 12), pady=12, sticky="nsew")

    card4 = create_status_card(root, app.t("system_status"), app.t("system_ready"))
    card4.grid(row=4, column=1, padx=(12, 24), pady=12, sticky="nsew")