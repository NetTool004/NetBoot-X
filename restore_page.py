import customtkinter as ctk


def build_restore_page(parent, app):
    root = ctk.CTkFrame(parent, fg_color="#03163d", corner_radius=22)
    root.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

    title = ctk.CTkLabel(
        root,
        text=app.t("restore_title"),
        font=ctk.CTkFont(size=24, weight="bold"),
        anchor="w"
    )
    title.pack(fill="x", padx=24, pady=(22, 6))

    desc = ctk.CTkLabel(
        root,
        text=app.t("restore_desc"),
        font=ctk.CTkFont(size=15),
        text_color="#9cc9ff",
        anchor="w"
    )
    desc.pack(fill="x", padx=24, pady=(0, 18))

    box = ctk.CTkFrame(root, fg_color="#0a245a", corner_radius=18)
    box.pack(fill="x", padx=24, pady=10)

    note = ctk.CTkLabel(
        box,
        text=app.t("restore_note"),
        font=ctk.CTkFont(size=16),
        anchor="w"
    )
    note.pack(fill="x", padx=18, pady=18)

    action_btn = ctk.CTkButton(
        root,
        text=app.t("restore_all"),
        height=42,
        fg_color="#3c8fe6",
        hover_color="#4ea0f5",
        command=app.restore_all
    )
    action_btn.pack(padx=24, pady=18, anchor="w")