import customtkinter
from app.inventory_management import show_manage_staff_screen

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")


class CreateNavigationPane:
    def __init__(
            self,
            app,
            show_dashboard_screen,
            show_manage_screen,
            show_profile_screen,
            show_settings_screen,
            show_manage_staff_screen=None,
            show_generate_report_screen=None,
    ):
        self.app = app
        self.active_button = None
        self.show_manage_staff_screen = show_manage_staff_screen

        # Navigation pane setup
        self.nav_frame = customtkinter.CTkFrame(
            app,
            width=220,
            corner_radius=0,
            fg_color="transparent"
        )
        self.nav_frame.pack(side="left", fill="y")

        # Navigation Header
        self.nav_header = customtkinter.CTkLabel(
            self.nav_frame,
            text="Menu",
            font=("Verdana", 20, "bold"),
            text_color=self.get_text_color(),
            fg_color="transparent"
        )
        self.nav_header.pack(pady=20, fill="x")

        # Define navigation buttons
        nav_buttons = [
            {"text": "Dashboard", "command": lambda: self.navigate(show_dashboard_screen, btn_index=0)},
            {"text": "Manage Inventory", "command": lambda: self.navigate(show_manage_screen, btn_index=1)},
            {"text": "Profile", "command": lambda: self.navigate(show_profile_screen, btn_index=2)},
            {"text": "Settings", "command": lambda: self.navigate(show_settings_screen, btn_index=3)},
        ]

        # Add supervisor options if applicable
        if self.show_manage_staff_screen:
            nav_buttons.append(
                {"text": "Manage Staff", "command": lambda: self.navigate(self.show_manage_staff_screen, btn_index=4)}
            )
        if show_generate_report_screen:
            nav_buttons.append(
                {"text": "Generate Report", "command": lambda: self.navigate(show_generate_report_screen, btn_index=5)}
            )

        # Create and style navigation buttons
        self.nav_buttons = []
        for i, btn_info in enumerate(nav_buttons):
            btn = customtkinter.CTkButton(
                self.nav_frame,
                text=btn_info["text"],
                command=btn_info["command"],
                height=40,
                width=220,
                font=("Verdana", 16),
                text_color=self.get_text_color(),
                fg_color="transparent",
                hover_color="#34495e",
                corner_radius=0,
                border_width=0
            )
            btn.pack(fill="x", pady=(0, 2))
            self.nav_buttons.append(btn)

        # Add Logout button at the bottom
        self.logout_button = customtkinter.CTkButton(
            self.nav_frame,
            text="Log Out",
            command=lambda: self.navigate(app.show_login_screen, btn_index=None),
            height=40,
            width=220,
            font=("Verdana", 16),
            text_color="#ffffff",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            corner_radius=0,
            border_width=0
        )
        self.logout_button.pack(side="bottom", fill="x", pady=(10, 0))

        # Assign nav_frame to app for access and clearing later
        app.nav_frame = self.nav_frame

        # Apply initial styles to buttons
        self.style_buttons()

    def get_text_color(self):
        mode = customtkinter.get_appearance_mode()
        return "#ffffff" if mode == "Dark" else "black"

    def navigate(self, screen_command, btn_index=None):
        """
        Navigates to a specified screen and updates the navigation button state.

        Args:
            screen_command (callable): The function to execute for navigating to the desired screen.
            btn_index (int, optional): The index of the navigation button to highlight. Defaults to None.
        """
        if screen_command and callable(screen_command):
            try:
                # Ensure the app window exists and execute the screen command
                if hasattr(self.app, 'winfo_exists') and self.app.winfo_exists():
                    # Clear frames if not navigating to the report generation screen
                    if screen_command != self.app.show_generate_report_screen:
                        self.app.clear_frames(exclude_nav=True)
                    screen_command()
            except Exception as e:
                print(f"Error executing screen command: {e}")
        else:
            print("Invalid screen command provided.")

        # Update button styles and set the active button if applicable
        self.style_buttons()

        if btn_index is not None and hasattr(self, 'nav_buttons') and self.nav_buttons:
            self.set_active_button(btn_index)

    def destroy(self):
        if hasattr(self, 'nav_frame') and self.nav_frame.winfo_exists():
            for widget in self.nav_frame.winfo_children():
                widget.destroy()

    def style_buttons(self):
        text_color = "#FFFFFF" if customtkinter.get_appearance_mode() == "Dark" else "#000000"

        if hasattr(self, 'nav_header') and self.nav_header.winfo_exists():
            try:
                self.nav_header.configure(text_color=text_color)
            except Exception as e:
                print(f"Error configuring nav_header: {e}")

    def set_active_button(self, btn_index):
        # Reset all buttons to default appearance first
        if hasattr(self, 'nav_buttons') and self.nav_buttons:
            for button in self.nav_buttons:
                if button.winfo_exists():  # Check if the button still exists
                    button.configure(
                        fg_color="transparent",
                        hover_color="#34495e"  # Set to default hover color
                    )

        # Check if the specified button index is within the bounds of the nav_buttons list
        if len(self.nav_buttons) > btn_index:
            self.active_button = self.nav_buttons[btn_index]
            if self.active_button.winfo_exists():  # Ensure the button exists
                self.active_button.configure(
                    fg_color="grey",  # Active button color
                    hover_color="#16a085"  # Active button hover color
                )
                self.style_buttons()  # Refresh the styles to apply changes
