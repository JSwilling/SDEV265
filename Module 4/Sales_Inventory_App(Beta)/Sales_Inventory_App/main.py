import tkinter as tk
import customtkinter
import pygame
from login import LoginScreen
from navigation import create_navigation_pane
from dashboard import DashboardScreen
from inventory_management import ManageInventoryScreen
from settings import SettingsScreen
from profile import ProfileScreen
from database import create_database
from backend import Backend
from terminate_user import TerminateUserScreen
from tkinter import messagebox

# Initialize Pygame mixer at the start of the script
pygame.mixer.init()

# Initialize backend
backend = Backend()

def play_audio(file_path):
    """Play an audio file using pygame."""
    try:
        pygame.mixer.music.load(r"Module 4\Sales_Inventory_App(Beta)\Sales_Inventory_App\test.mp3")
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing audio file: {e}")

class InventoryApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title("Inventory Management System")
        self.resizable(False, False)  # Disable maximize button on the login screen
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        self.current_user = None
        self.current_user_role = None
        self.nav_frame = None
        self.is_full_screen = False
        create_database()
        self.backend = Backend()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Removed redundant LoginScreen initialization
        # LoginScreen(self, self.login_success_callback)

        # Play startup jingle
        play_audio("test.mp3")

        self.show_login_screen()

        # Apply the border with glow effect
        self.configure(bg="#1abc9c")  # Border color similar to login screen
        self.update_idletasks()

        # Set the app to be on top at startup
        self.lift()  # Raise the window
        self.attributes('-topmost', True)  # Ensure the window stays on top
        self.after(1000, lambda: self.attributes('-topmost', False))  # Remove the "always on top" after 1 second

    def on_close(self):
        # Play logout sound before closing
        play_audio("log_out_sound.mp3")
        self.after(1000, self.destroy)

    def show_login_screen(self):
        self.geometry("398x648")
        self.resizable(False, False)  # Keep maximize button disabled on the login screen
        self.clear_frames()
        LoginScreen(self, self.login_success_callback)

    def login_success_callback(self, username, role):
        print(f"Logged in as {username} with role {role}")
        self.current_user = username
        self.current_user_role = role

        # Remove `overrideredirect` flag before moving to the next screen
        self.overrideredirect(False)
        self.show_dashboard_screen()

    def show_dashboard_screen(self):
        self.geometry("1000x700")  # Resize window for the dashboard
        self.resizable(True, True)  # Enable maximize button after login
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        DashboardScreen(self)

    def show_manage_screen(self):
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        ManageInventoryScreen(self, self.backend)

    def show_profile_screen(self):
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        ProfileScreen(self, self.current_user, self.current_user_role)

    def show_settings_screen(self):
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        SettingsScreen(self, self.current_user_role, self.backend)

    def show_terminate_screen(self):
        if self.current_user_role == 'Supervisor':
            self.clear_frames(exclude_nav=True)
            self.create_or_update_navigation_pane()
            TerminateUserScreen(self, self.backend)

    def clear_frames(self, exclude_nav=False):
        # Clear all frames except navigation if specified
        for widget in self.winfo_children():
            if exclude_nav and self.nav_frame and widget == self.nav_frame:
                continue
            try:
                widget.destroy()
            except Exception as e:
                print(f"Error destroying widget: {e}")
        if not exclude_nav and self.nav_frame:
            try:
                self.nav_frame.destroy()
                self.nav_frame = None
            except Exception as e:
                print(f"Error destroying nav_frame: {e}")

    def create_or_update_navigation_pane(self):
        # Destroy the existing nav_frame before creating a new one
        if self.nav_frame:
            try:
                self.nav_frame.destroy()
            except Exception as e:
                print(f"Error destroying nav_frame: {e}")

        self.nav_frame = create_navigation_pane(
            self,
            self.show_dashboard_screen,
            self.show_manage_screen,
            self.show_profile_screen,
            self.show_settings_screen,
            self.show_terminate_screen if self.current_user_role == "Supervisor" else None,
        )

    def toggle_fullscreen(self):
        # Toggle between fullscreen and windowed mode
        if self.is_full_screen:
            self.attributes("-fullscreen", False)
            self.is_full_screen = False
        else:
            self.attributes("-fullscreen", True)
            self.is_full_screen = True

    def apply_glow_effect(self):
        colors = ["#34495e", "#5a9ea3", "#7fc6c3", "#a1e0dd", "#1abc9c"]
        delay = 100  # Time between color changes in milliseconds

        def animate(index=0):
            self.configure(border_color=colors[index % len(colors)])
            self.after(delay, lambda: animate(index + 1))

        self.configure(border_width=5)
        animate()


if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
