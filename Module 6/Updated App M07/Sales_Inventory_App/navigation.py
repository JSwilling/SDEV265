import customtkinter
import pywinstyles
import sys
import tkinter as tk


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
            show_terminate_screen=None,
            show_generate_report_screen=None,
    ):
        self.app = app
        self.active_button = None

        # Navigation pane setup
        self.nav_frame = customtkinter.CTkFrame(
            app,
            width=220,
            corner_radius=0,
            fg_color="transparent"  # Transparent background color for the navigation pane

        )
        self.nav_frame.pack(side="left", fill="y")

        # Navigation Header
        self.nav_header = customtkinter.CTkLabel(
            self.nav_frame,
            text="Menu",
            font=("Verdana", 20, "bold"),
            text_color=self.get_text_color(),  # Set header text color dynamically
            fg_color="transparent"  # Transparent background
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
        if show_terminate_screen:
            nav_buttons.append(
                {"text": "Terminate User", "command": lambda: self.navigate(show_terminate_screen, btn_index=4)})
        if show_generate_report_screen:
            nav_buttons.append(
                {"text": "Generate Report", "command": lambda: self.navigate(show_generate_report_screen, btn_index=5)})

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
                text_color=self.get_text_color(),  # Set button text color dynamically
                fg_color="transparent",  # Make button background transparent to remove white boxes
                hover_color="#34495e",  # Slightly lighter color for hover
                corner_radius=0,  # Keep sharp corners to match the design
                border_width=0  # Remove any borders
            )
            btn.pack(fill="x", pady=(0, 2))  # Reduced padding to eliminate gaps
            self.nav_buttons.append(btn)

        # Add Logout button at the bottom
        self.logout_button = customtkinter.CTkButton(
            self.nav_frame,
            text="Log Out",
            command=lambda: self.navigate(app.show_login_screen, btn_index=None),
            height=40,
            width=220,
            font=("Verdana", 16),
            text_color="#ffffff",  # Keep logout button text white for contrast
            fg_color="#e74c3c",  # Bright red to distinguish it
            hover_color="#c0392b",  # Darker red for hover effect
            corner_radius=0,
            border_width=0
        )
        self.logout_button.pack(side="bottom", fill="x", pady=(10, 0))

        # Assign nav_frame to app for access and clearing later
        app.nav_frame = self.nav_frame

        # Apply initial styles to buttons
        self.style_buttons()

    def get_text_color(self):
        """Get the appropriate text color based on the current appearance mode."""
        mode = customtkinter.get_appearance_mode()
        if mode == "Dark":
            return "#ffffff"  # White text for dark mode
        else:
            return "black"  # Black text for light mode

    def navigate(self, screen_command, btn_index=None):
        # Only clear frames if we are not generating a report
        if screen_command != self.app.show_generate_report_screen:
            self.app.clear_frames(exclude_nav=True)
        screen_command()

        # Reapply styles to navigation buttons to ensure consistency
        self.style_buttons()

        # Highlight the active button
        if btn_index is not None:
            self.set_active_button(btn_index)

    def refresh_styles(self):
        """Refresh styles dynamically after theme change."""
        # Update text color dynamically based on current theme
        self.style_buttons()

    def style_buttons(self):
        """Reapply styles to all navigation buttons to maintain consistency."""
        text_color = self.get_text_color()
        self.nav_header.configure(text_color=text_color)  # Update header text color dynamically
        for btn in self.nav_buttons:
            btn.configure(
                text_color=text_color,  # Ensure text color is set dynamically
                fg_color="transparent",  # Set background to transparent
                hover_color="#34495e",  # Hover color for visual feedback
                border_width=0
            )

        # Style the logout button separately
        self.logout_button.configure(
            fg_color="#e74c3c",
            hover_color="#c0392b",
            border_width=0
        )

    def set_active_button(self, btn_index):
        """Set a different color for the active navigation button."""
        # Reset the previous active button (if any)
        if self.active_button is not None:
            self.active_button.configure(
                fg_color="transparent",  # Default button background color to transparent
                hover_color="#34495e"
            )

        # Highlight the new active button
        self.active_button = self.nav_buttons[btn_index]
        self.active_button.configure(
            fg_color="#1abc9c",  # Highlighted color for active button
            hover_color="#16a085"
        )

        # Update header and buttons' text color after switching modes
        self.style_buttons()
