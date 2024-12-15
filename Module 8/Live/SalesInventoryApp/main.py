import tkinter as tk
import customtkinter
import pygame
import sqlite3
from tkinter import ttk, filedialog, messagebox
from app.login import LoginScreen
from app.navigation import CreateNavigationPane
from app.dashboard import DashboardScreen
from app.settings import SettingsScreen
from app.profile import ProfileScreen
from app.terminate_user import TerminateUserScreen
from app.backend import Backend
from app.report import GenerateReportPopup
from app.inventory_management import ManageInventoryScreen
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.inventory_management import ManageStaffScreen
from app.database import initialize_database
import threading
from time import sleep
import time
from PIL import Image, ImageTk

# Initialize Pygame mixer at the start of the script
pygame.mixer.init()

customtkinter.set_appearance_mode("Light")  # or "Dark"
customtkinter.set_default_color_theme("blue")  # or any other theme

# Initialize backend
backend = Backend()
backend.create_database()
initialize_database()


class LoadingScreen:
    """A modern, frameless loading screen design."""
    def __init__(self, root):
        self.root = root
        self.stop_animation = False  # Flag to stop animation

        # Overlay Frame for full-screen loading
        self.loading_frame = customtkinter.CTkFrame(
            root,
            fg_color="#ffffff"
        )
        self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Compact Container for the loading screen content
        self.container = customtkinter.CTkFrame(
            self.loading_frame,
            corner_radius=10,
            fg_color="#ffffff"
        )
        self.container.pack(padx=20, pady=20)

        # Loading Label with modern styling
        self.loading_label = customtkinter.CTkLabel(
            self.container,
            text="Please Wait...",
            font=("Helvetica Neue", 14, "bold"),
            text_color="#c0392b"
        )
        self.loading_label.pack(pady=(10, 5))

        # Minimalist Progress Bar
        self.progress_bar = customtkinter.CTkProgressBar(
            self.container,
            orientation="horizontal",
            mode="indeterminate",
            width=150,
            fg_color="#c0392b",
            progress_color="#ffffff"
        )
        self.progress_bar.pack(pady=(5, 10))
        self.progress_bar.start()  # Start the animation

        # Optional Animated Icon (Simulated as "GIF animation")
        self.loading_icon = customtkinter.CTkLabel(
            self.container,
            text="🔄",
            font=("Arial", 20, "bold"),
            text_color="#c0392b"
        )
        self.loading_icon.pack()

        self.animate_gif()

        # Make the window frameless and center it
        self.root.overrideredirect(True)
        self.center_window(300, 200)

    def center_window(self, width, height):
        """Center the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def animate_gif(self):
        """Simulate GIF animation using a simple text rotation."""
        if not self.stop_animation:  # Check if the animation should stop
            current_text = self.loading_icon.cget("text")
            next_text = "🔄" if current_text != "🔄" else "🔁"  # Alternate icons
            self.loading_icon.configure(text=next_text)
            self.root.after(200, self.animate_gif)  # Repeat every 200ms

    def destroy(self):
        """Remove the loading screen and stop animation."""
        self.stop_animation = True  # Stop the animation loop
        self.loading_frame.destroy()



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

        # Play startup jingle
        self.play_audio(r"Module 8\STABLE (TESTING)\Sales_Inventory_App\test.mp3")


        # Apply the border with glow effect
        self.configure(bg="#1abc9c")  # Border color similar to login screen
        self.update_idletasks()

        # Set the app to be on top at startup
        self.lift()  # Raise the window
        self.attributes('-topmost', True)  # Ensure the window stays on top
        self.after(1000, lambda: self.attributes('-topmost', False))  # Remove the "always on top" after 1 second

        self.show_loading_screen()

    def show_loading_screen(self):
        """Show a loading screen while the app initializes."""
        self.loading_screen = LoadingScreen(self)

        # Simulate initialization tasks in a separate thread
        threading.Thread(target=self.initialize_app).start()


    def initialize_app(self):
        """Simulate initialization tasks."""
        for _ in range(3):  # Simulate a 4-second task in 1-second chunks
            time.sleep(1)  # Simulate delay
            self.after(0, self.update_loading_message, "Still loading...")

        # Complete initialization
        self.after(0, self.complete_initialization)

    def update_loading_message(self, message):
        """Update the loading screen message."""
        pass


    def complete_initialization(self):
        """Complete the app initialization and show the main screen."""
        self.show_login_screen()
        self.loading_screen.destroy()


    def play_audio(self, file_path):
        """Play an audio file using pygame."""
        try:
            pygame.mixer.music.load(r'static/audio/login.mp3')
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing audio file: {e}")

    def on_close(self):
        # Play logout sound before closing
        pygame.mixer.music.load(r'static/audio/logout.mp3')
        pygame.mixer.music.play()
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

        # Show the dashboard screen after successful login
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
        ManageInventoryScreen(self, backend, self.current_user_role, self.current_user)  # Pass username here

    def show_profile_screen(self):
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        ProfileScreen(self, self.current_user, self.current_user_role)

    def show_settings_screen(self):
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        SettingsScreen(self, self.current_user_role, backend)

    def show_manage_staff_screen(self):
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        ManageStaffScreen(self, backend, self.current_user_role)

    def refresh_styles(self):
        """Refresh styles for all components after theme change."""
        if hasattr(self, 'nav_frame') and isinstance(self.nav_frame, CreateNavigationPane):
            self.nav_frame.refresh_styles()

    def show_terminate_screen(self):
        if self.current_user_role == 'Supervisor':
            self.clear_frames(exclude_nav=True)
            self.create_or_update_navigation_pane()
            TerminateUserScreen(self, backend)

    def show_generate_report_screen(self):
        # Launch the GenerateReportScreen module
        report_screen = GenerateReportPopup(self)
        report_screen.mainloop()  # Start the main loop for the report screen
        print("Reports screen launched successfully.")

    def clear_frames(self, exclude_nav=False):
        # Clear all frames except navigation if specified
        for widget in self.winfo_children():
            if exclude_nav and self.nav_frame and widget == self.nav_frame:
                continue
            if str(widget) in self.tk.call('winfo', 'children', self):
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

        # Prepare parameters based on user role
        if self.current_user_role == "Supervisor":
            show_manage_staff_screen = self.show_manage_staff_screen
            show_generate_report_screen = self.show_generate_report_screen
        else:
            show_manage_staff_screen = None
            show_generate_report_screen = None

        # Instantiate the navigation pane with the correct parameters
        self.nav_frame = CreateNavigationPane(
            self,
            self.show_dashboard_screen,
            self.show_manage_screen,
            self.show_profile_screen,
            self.show_settings_screen,
            show_manage_staff_screen=show_manage_staff_screen,
            show_generate_report_screen=show_generate_report_screen
        )


    def toggle_fullscreen(self):
        # Toggle between fullscreen and windowed mode
        if self.is_full_screen:
            self.attributes("-fullscreen", False)
            self.is_full_screen = False
        else:
            self.attributes("-fullscreen", True)
            self.is_full_screen = True


if __name__ == "__main__":
    app = InventoryApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Set up proper window close handling
    app.mainloop()
