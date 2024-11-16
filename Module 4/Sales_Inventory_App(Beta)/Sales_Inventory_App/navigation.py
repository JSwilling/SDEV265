# navigation.py
import customtkinter

def create_navigation_pane(
    app,
    show_dashboard_screen,
    show_manage_screen,
    show_profile_screen,
    show_settings_screen,
    show_terminate_screen=None
):
    # Navigation pane setup
    nav_frame = customtkinter.CTkFrame(
        app,
        width=220,
        corner_radius=0,
        fg_color="#2c3e50"  # Dark background color
    )
    nav_frame.pack(side="left", fill="y")

    # Navigation Header
    nav_header = customtkinter.CTkLabel(
        nav_frame,
        text="Menu",
        font=("Verdana", 20, "bold"),
        text_color="#ecf0f1"
    )
    nav_header.pack(pady=20)

    # Define navigation buttons
    nav_buttons = [
        {"text": "Dashboard", "command": show_dashboard_screen},
        {"text": "Manage Inventory", "command": show_manage_screen},
        {"text": "Profile", "command": show_profile_screen},
        {"text": "Settings", "command": show_settings_screen},
    ]

    # Add "Terminate User" option for supervisors
    if show_terminate_screen:
        nav_buttons.append({"text": "Terminate User", "command": show_terminate_screen})

    # Create navigation buttons
    for btn_info in nav_buttons:
        btn = customtkinter.CTkButton(
            nav_frame,
            text=btn_info["text"],
            command=btn_info["command"],
            corner_radius=0,
            height=50,
            width=220,
            fg_color="#2c3e50",       # Match nav pane background for flat design
            hover_color="#34495e",     # Slightly lighter on hover
            text_color="#ecf0f1",
            font=("Verdana", 16),
            anchor="w",                # Align text to the left
            border_spacing=10          # Add padding between the icon/text and the button edge
        )
        btn.pack(fill="x", pady=5)

    # Add Logout button at the bottom
    logout_button = customtkinter.CTkButton(
        nav_frame,
        text="Log Out",
        command=app.show_login_screen,
        corner_radius=0,
        height=50,
        width=220,
        fg_color="#e74c3c",       # Red color for logout
        hover_color="#c0392b",
        text_color="#ecf0f1",
        font=("Verdana", 16),
        anchor="w",
        border_spacing=10
    )
    logout_button.pack(side="bottom", fill="x", pady=10)

    # Assign nav_frame to app so it can be accessed and cleared later
    app.nav_frame = nav_frame
