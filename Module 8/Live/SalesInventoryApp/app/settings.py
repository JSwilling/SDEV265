import customtkinter
import tkinter as tk
from tkinter import ttk
import tkinter.ttk as ttk
import sqlite3
import datetime
from tkcalendar import Calendar
import bcrypt
import base64
from tkinter import filedialog
import os
import shutil
from tkinter import messagebox



class SettingsScreen:
    def __init__(self, app, user_role, backend):
        self.app = app
        self.user_role = user_role
        self.backend = backend

        # Settings Frame
        self.settings_frame = customtkinter.CTkFrame(
            self.app, corner_radius=20, border_width=2, border_color="#2ECC71", fg_color="#F8F9FA"
        )
        self.settings_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Settings Header
        settings_label = customtkinter.CTkLabel(
            self.settings_frame, text="Settings", font=("Arial", 26, "bold"), text_color="#2C3E50"
        )
        settings_label.pack(pady=20)

        # Profile Settings Section
        self.add_section_label("Profile Settings")
        upload_photo_button = customtkinter.CTkButton(
            self.settings_frame, text="Upload Profile Photo", command=self.upload_photo, width=200, height=50,
            corner_radius=10, fg_color="#3498DB", hover_color="#2980B9", text_color="#FFFFFF"
        )
        upload_photo_button.pack(pady=10)

        # Application Actions Section
        self.add_section_label("Application Actions")
        logout_button = customtkinter.CTkButton(
            self.settings_frame, text="Log Out", command=self.logout_with_audio, width=200, height=50,
            corner_radius=10, fg_color="#E67E22", hover_color="#D35400", text_color="#FFFFFF"
        )
        logout_button.pack(pady=10)

        close_app_button = customtkinter.CTkButton(
            self.settings_frame, text="Close App", command=self.close_app_with_audio, width=200, height=50,
            corner_radius=10, fg_color="#34495E", hover_color="#2C3E50", text_color="#FFFFFF"
        )
        close_app_button.pack(pady=10)

        # Supervisor-Specific Actions
        if self.user_role == "Supervisor":
            self.add_section_label("Supervisor Actions")
            self.add_clear_db_button()

    def add_section_label(self, text):
        """Helper to add section headers."""
        section_label = customtkinter.CTkLabel(
            self.settings_frame, text=text, font=("Arial", 18, "bold"), text_color="#34495E"
        )
        section_label.pack(pady=15)

    def add_clear_db_button(self):
        """Add the CLEAR DB button for supervisors."""
        clear_db_button = customtkinter.CTkButton(
            self.settings_frame,
            text="CLEAR DB",
            command=self.confirm_clear_db,
            width=200,
            height=50,
            corner_radius=10,
            fg_color="#F1C40F",  # Yellow
            hover_color="#F39C12",
            text_color="#E74C3C",  # Red text
            border_width=2,
            border_color="#000000",  # Black border
        )
        clear_db_button.pack(pady=20)

    def confirm_clear_db(self):
        """Popup confirmation before clearing the database."""
        confirm = messagebox.askyesno(
            "Confirm Clear DB",
            "Are you sure you want to clear the database? This action cannot be undone.",
        )
        if confirm:
            self.clear_database()

    def clear_database(self):
        """Clear all tables in the database and recreate them."""
        try:
            # Ensure the database connection is open
            self.backend.connect()

            # Drop all existing tables
            self.backend.cursor.execute("DROP TABLE IF EXISTS users")
            self.backend.cursor.execute("DROP TABLE IF EXISTS InventoryItem")
            self.backend.cursor.execute("DROP TABLE IF EXISTS Customers")
            self.backend.cursor.execute("DROP TABLE IF EXISTS clock_items")
            self.backend.cursor.execute("DROP TABLE IF EXISTS user_activity")
            self.backend.cursor.execute("DROP TABLE IF EXISTS Orders")
            self.backend.conn.commit()

            # Recreate the database schema
            self.backend.create_database()

            # Hash and encode the default password
            default_password = "TESTING"
            hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
            hashed_password_base64 = base64.b64encode(hashed_password).decode('utf-8')

            # Add a default user account
            self.backend.cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("Admin", hashed_password_base64, "Supervisor")
            )
            self.backend.conn.commit()

            # Show success message
            messagebox.showinfo("Success", "The database has been cleared and recreated successfully.")
        except Exception as e:
            # Show error message
            messagebox.showerror("Error", f"Failed to clear the database: {e}")
        finally:
            # Ensure the connection is closed even if an error occurs
            if self.backend.conn:
                self.backend.disconnect()

    def upload_photo(self):
        """Upload a profile photo and save it for the current user."""
        file_path = filedialog.askopenfilename(
            title="Select a Profile Photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            try:
                if not os.path.exists("../static/images"):
                    os.makedirs("../static/images")
                dest_path = os.path.join("../static/images", f"{self.app.current_user}_profile_photo.png")
                shutil.copy(file_path, dest_path)
                messagebox.showinfo("Upload Photo", f"Photo successfully uploaded for {self.app.current_user}.")
            except Exception as e:
                messagebox.showerror("Upload Error", f"Failed to upload photo: {e}")
        else:
            messagebox.showwarning("Upload Photo", "No photo was selected.")

    def logout_with_audio(self):
        try:
            pygame.mixer.music.load(r'static/audio/logout.mp3')
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing logout audio: {e}")
        finally:
            self.app.show_login_screen()

    def close_app_with_audio(self):
        try:
            pygame.mixer.music.load(r'static/audio/logout.mp3')
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing close app audio: {e}")
        finally:
            self.app.quit()
