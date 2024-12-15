import customtkinter
import pywinstyles
import sys


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class create_navigation_pane:
    def __init__(
            self,
            app,
            show_dashboard_screen,
            show_manage_screen,
            show_profile_screen,
            show_settings_screen,
            show_terminate_screen=None,
            show_generate_report_screen=None,
    ):
        self.app = app

        # Initialize styles
        self.init_styles()

        # Navigation pane setup
        self.nav_frame = customtkinter.CTkFrame(
            app,
            width=220,
            corner_radius=0,
            fg_color=self.nav_bg_color,
            bg_color=self.nav_bg_color,
        )
        self.nav_frame.pack(side="left", fill="y")

        # Navigation Header
        nav_header = customtkinter.CTkLabel(
            self.nav_frame,
            text="Menu",
            font=self.header_font,
            text_color=self.text_color,
            fg_color="transparent",
            bg_color="transparent",
        )
        nav_header.pack(pady=20)

        # Define navigation buttons
        nav_buttons = [
            {"text": "Dashboard", "command": show_dashboard_screen},
            {"text": "Manage Inventory", "command": show_manage_screen},
            {"text": "Profile", "command": show_profile_screen},
            {"text": "Settings", "command": show_settings_screen},
        ]

        # Add supervisor options
        if show_terminate_screen:
            nav_buttons.append({"text": "Terminate User", "command": show_terminate_screen})
        if show_generate_report_screen:
            nav_buttons.append({"text": "Generate Report", "command": show_generate_report_screen})

        # Create navigation buttons
        self.nav_buttons = []
        for btn_info in nav_buttons:
            btn = customtkinter.CTkButton(
                self.nav_frame,
                text=btn_info["text"],
                command=btn_info["command"],
                corner_radius=0,
                height=50,
                width=220,
                font=self.button_font,
                anchor="w",
                border_spacing=10,
                fg_color=self.nav_bg_color,
                bg_color=self.nav_bg_color,
                hover_color=self.hover_color,
                text_color=self.text_color,
            )
            btn.pack(fill="x", pady=5)
            self.nav_buttons.append(btn)

            # Apply opacity using pywinstyles
            try:
                pywinstyles.set_opacity(btn, color=self.nav_bg_color)
            except Exception as e:
                print(f"Failed to set opacity on button '{btn_info['text']}': {e}")

        # Add Logout button at the bottom
        self.logout_button = customtkinter.CTkButton(
            self.nav_frame,
            text="Log Out",
            command=app.show_login_screen,
            corner_radius=0,
            height=50,
            width=220,
            font=self.button_font,
            anchor="w",
            border_spacing=10,
            fg_color="#e74c3c",
            bg_color=self.nav_bg_color,
            hover_color=self.logout_hover_color,
            text_color=self.text_color,
        )
        self.logout_button.pack(side="bottom", fill="x", pady=10)

        # Apply opacity to the logout button
        try:
            pywinstyles.set_opacity(self.logout_button, color=self.nav_bg_color)
        except Exception as e:
            print(f"Failed to set opacity on 'Log Out' button: {e}")

        # Assign nav_frame to app so it can be accessed and cleared later
        app.nav_frame = self.nav_frame

    def init_styles(self):
        """Initialize dynamic styles for the navigation pane."""
        # Colors
        self.nav_bg_color = "#2c3e50"  # Navigation pane background
        self.hover_color = "#34495e"  # Button hover color
        self.text_color = "#ecf0f1"  # Text color
        self.logout_hover_color = "#c0392b"  # Logout hover color

        # Fonts
        self.header_font = ("Verdana", 20, "bold")
        self.button_font = ("Verdana", 16)


class NavigationPane:
    def __init__(self, app,):
        self.logout_hover_color = None
        self.logout_fg_color = None
        self.text_color = None
        self.hover_color = None
        self.nav_bg_color = None
        self.app = app

        # Navigation pane setup
        self.nav_frame = tk.Frame(
            app,
            width=220,
            bg="#2c3e50"
        )
        self.nav_frame.pack(side="left", fill="y")

        # Navigation Header
        nav_header = tk.Label(
            self.nav_frame,
            text="Menu",
            font=("Verdana", 20, "bold"),
            fg="transparent",
            bg="#2c3e50"
        )
        nav_header.pack(pady=20)

        # Add Logout button at the bottom
        logout_button = tk.Button(
            self.nav_frame,
            text="Log Out",
            command=app.show_login_screen,
            font=("Verdana", 16),
            anchor="w",
            padx=10,
            fg="#ecf0f1",
            bg="#e74c3c",
            activebackground="#c0392b",
            activeforeground="#ecf0f1",
            relief="flat"
        )
        logout_button.pack(side="bottom", fill="x", pady=10)

    def init_styles(self):
        """Initialize dynamic styles for the navigation pane."""
        # Colors
        self.nav_bg_color = "#2c3e50"  # Navigation pane background
        self.hover_color = "#34495e"  # Button hover color
        self.text_color = "#ecf0f1"  # Text color
        self.logout_fg_color = "#e74c3c"  # Logout button color
        self.logout_hover_color = "#c0392b"  # Logout hover color

        # Fonts
        self.header_font = ("Verdana", 20, "bold")
        self.button_font = ("Verdana", 16)

    def update_styles(self, new_theme):
        """Update styles dynamically at runtime."""
        # Update style variables based on the new theme
        if new_theme == "dark":
            self.nav_bg_color = "#2c3e50"
            self.hover_color = "#34495e"
            self.text_color = "#ecf0f1"
        elif new_theme == "light":
            self.nav_bg_color = "#ecf0f1"
            self.hover_color = "#bdc3c7"
            self.text_color = "#2c3e50"
        # Re-apply styles
        self.nav_frame.configure(fg_color=self.nav_bg_color)
        self.style_buttons()

    def style_buttons(self):
        """Apply styles to navigation buttons dynamically."""
        for btn in self.nav_buttons:
            btn.configure(
                fg_color=self.nav_bg_color,
                bg_color=self.nav_bg_color,
                hover_color=self.hover_color,
                text_color=self.text_color
            )

            self.app.after(100, self._apply_styles)

        # Style the logout button separately
        self.logout_button.configure(
            fg_color=self.logout_fg_color,
            bg_color=self.nav_bg_color,
            hover_color=self.logout_hover_color,
            text_color=self.text_color
        )

        def _apply_styles(self):
            for btn in self.nav_buttons:
                btn.configure(
                    hover_color=self.hover_color,
                    text_color=self.text_color
                )
            # Style the logout button separately
            self.logout_button.configure(
                fg_color="#e74c3c",
                hover_color=self.logout_hover_color,
                text_color=self.text_color
            )