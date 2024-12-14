import customtkinter
import os
from PIL import Image, ImageTk
import shutil
from tkinter import filedialog, messagebox
import sqlite3
from datetime import datetime
import sqlite3
import bcrypt
import base64

class ProfileScreen:
    def __init__(self, app, username, role):
        self.app = app
        self.username = username
        self.role = role

        # Profile Frame
        self.profile_frame = customtkinter.CTkFrame(self.app, corner_radius=15, border_width=3, border_color="#c0392b")
        self.profile_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Profile Header with Role
        self.profile_header_label = customtkinter.CTkLabel(
            self.profile_frame,
            text=f" {self.username} Role: {self.role}",
            font=("Arial", 24, "bold"),
            text_color="#34495e",
        )
        self.profile_header_label.pack(pady=10)

        # Content Frame for layout
        content_frame = customtkinter.CTkFrame(self.profile_frame, corner_radius=10)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Section: Profile Photo and Work Hours
        self.create_left_section(content_frame)

        # Right Section: Recent Activity and Updates
        self.create_right_section(content_frame)

    def create_left_section(self, parent):
        """Left section with Profile Photo and Work Hours."""
        left_section = customtkinter.CTkFrame(parent, fg_color="#ecf0f1")
        left_section.pack(side="left", fill="both", expand=False, padx=10, pady=10)

        # Profile Photo
        customtkinter.CTkLabel(
            left_section,
            text="",  # Ensure no text is set here
            font=("Arial", 18, "bold"),
            text_color="#34495e",
        ).pack(pady=5)

        image_path = self.get_profile_photo_path()
        if os.path.exists(image_path):
            image = Image.open(image_path).resize((150, 150))
            self.profile_photo = ImageTk.PhotoImage(image)
            profile_photo_label = customtkinter.CTkLabel(left_section, image=self.profile_photo, text="")
        else:
            profile_photo_label = customtkinter.CTkLabel(
                left_section,
                text="No Profile Photo",  # Only set text if no photo is available
                width=150,
                height=150,
                corner_radius=15,
                fg_color="#dfe6e9",
            )
        profile_photo_label.pack(pady=5)

        # Work Hours Buttons
        customtkinter.CTkLabel(
            left_section,
            text="Work Hours",
            font=("Arial", 18, "bold"),
            text_color="#34495e",
        ).pack(pady=10)

        clock_in_button = customtkinter.CTkButton(
            left_section,
            text="Clock In",
            command=self.clock_in,
            fg_color="#2ECC71",
            text_color="#ffffff",
        )
        clock_in_button.pack(pady=5)

        clock_out_button = customtkinter.CTkButton(
            left_section,
            text="Clock Out",
            command=self.clock_out,
            fg_color="#E74C3C",
            text_color="#ffffff",
        )
        clock_out_button.pack(pady=5)

    def create_right_section(self, parent):
        """Right section with Recent Activity and Updates."""
        right_section = customtkinter.CTkFrame(parent, fg_color="#ffffff")
        right_section.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Recent Activity
        customtkinter.CTkLabel(
            right_section,
            text="Recent Activity",
            font=("Arial", 18, "bold"),
            text_color="#34495e",
        ).pack(pady=5)

        self.activity_frame = customtkinter.CTkFrame(right_section, fg_color="#ffffff")
        self.activity_frame.pack(fill="x", expand=False, padx=5, pady=5)
        self.load_recent_activity()

        # Username and Password Updates
        update_frame = customtkinter.CTkFrame(right_section, fg_color="#f7f9fc")
        update_frame.pack(fill="x", padx=5, pady=10)

        # Username Update Section
        customtkinter.CTkLabel(
            update_frame,
            text="Update Username",
            font=("Arial", 18, "bold"),
            text_color="#34495e",
        ).grid(row=0, column=0, columnspan=2, pady=5)

        self.new_username_entry = customtkinter.CTkEntry(
            update_frame,
            placeholder_text="Enter new username",
            width=200,
            corner_radius=10,
        )
        self.new_username_entry.grid(row=1, column=0, padx=10, pady=5)

        update_username_button = customtkinter.CTkButton(
            update_frame,
            text="Update Username",
            command=self.update_username,
            fg_color="#1abc9c",
            text_color="#ffffff",
        )
        update_username_button.grid(row=1, column=1, padx=10, pady=5)

        # Password Update Section
        customtkinter.CTkLabel(
            update_frame,
            text="Update Password",
            font=("Arial", 18, "bold"),
            text_color="#34495e",
        ).grid(row=2, column=0, columnspan=2, pady=5)

        self.old_password_entry = customtkinter.CTkEntry(
            update_frame,
            placeholder_text="Enter old password",
            show="*",
            width=200,
            corner_radius=10,
        )
        self.old_password_entry.grid(row=3, column=0, padx=10, pady=5)

        self.new_password_entry = customtkinter.CTkEntry(
            update_frame,
            placeholder_text="Enter new password",
            show="*",
            width=200,
            corner_radius=10,
        )
        self.new_password_entry.grid(row=3, column=1, padx=10, pady=5)

        self.confirm_password_entry = customtkinter.CTkEntry(
            update_frame,
            placeholder_text="Confirm new password",
            show="*",
            width=200,
            corner_radius=10,
        )
        self.confirm_password_entry.grid(row=4, column=0, padx=10, pady=5)

        update_password_button = customtkinter.CTkButton(
            update_frame,
            text="Update Password",
            command=self.update_password,
            fg_color="#1abc9c",
            text_color="#ffffff",
        )
        update_password_button.grid(row=4, column=1, padx=10, pady=5)

    def update_password(self):
        """Handle updating the password."""
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not old_password or not new_password or not confirm_password:
            messagebox.showerror("Error", "All password fields are required.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match.")
            return

        if len(new_password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return

        conn = sqlite3.connect(r'db/Sales_Inventory.db')
        cursor = conn.cursor()

        # Fetch the current hashed password
        cursor.execute("SELECT password FROM users WHERE username = ?", (self.username,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "User not found.")
            conn.close()
            return

        # Verify the old password
        stored_hashed_password = base64.b64decode(result[0].encode('utf-8'))
        if not bcrypt.checkpw(old_password.encode('utf-8'), stored_hashed_password):
            messagebox.showerror("Error", "Old password is incorrect.")
            conn.close()
            return

        # Hash the new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        hashed_password_base64 = base64.b64encode(hashed_password).decode('utf-8')

        # Update the password in the database
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password_base64, self.username))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password updated successfully.")

    def get_profile_photo_path(self):
        """Path where the profile photo is stored."""
        return os.path.join("../static/images", f"{self.username}_profile_photo.png")
    def update_username(self):
        """Handle updating the username."""
        new_username = self.new_username_entry.get()
        if not new_username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        conn = sqlite3.connect(r'db/Sales_Inventory.db')
        cursor = conn.cursor()

        # Check if the username is already taken
        cursor.execute("SELECT * FROM users WHERE username = ?", (new_username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already taken.")
            conn.close()
            return

        # Update the username in the database
        cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, self.username))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Username updated successfully.")
        self.username = new_username  # Update the current username
        self.app.current_user = new_username
        # Refresh the profile header to show the updated username
        self.profile_header_label.configure(text=f"Profile: {self.username} (Role: {self.role})")

    def get_profile_photo_path(self):
        """Path where the profile photo is stored."""
        return os.path.join("../static/images", f"{self.username}_profile_photo.png")



    def clock_in(self):
        """Log the user as clocked in."""
        self.record_action("Clocked In")
        conn = sqlite3.connect(r'db/Sales_Inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clock_times (username, clock_in) VALUES (?, ?)", (self.username, datetime.now()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Clock In", "You have successfully clocked in.")

    def clock_out(self):
        """Log the user as clocked out."""
        self.record_action("Clocked Out")
        conn = sqlite3.connect(r'db/Sales_Inventory.db')
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clock_times SET clock_out = ? WHERE username = ? AND clock_out IS NULL",
            (datetime.now(), self.username),
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Clock Out", "You have successfully clocked out.")

    def record_action(self, action):
        """Record the user's action in the activity log."""
        conn = sqlite3.connect(r'db/Sales_Inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_activity (username, action) VALUES (?, ?)", (self.username, action))
        conn.commit()
        conn.close()
        self.load_recent_activity()

    def load_recent_activity(self):
        """Load and display the recent activities of the user."""
        for widget in self.activity_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect(r'db/Sales_Inventory.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT action, timestamp FROM user_activity WHERE username = ? ORDER BY timestamp DESC LIMIT 5",
            (self.username,),
        )
        activities = cursor.fetchall()
        conn.close()

        for action, timestamp in activities:
            customtkinter.CTkLabel(
                self.activity_frame,
                text=f"{timestamp}: {action}",
                font=("Arial", 14),
                text_color="#34495e",
            ).pack(anchor="w", pady=2)


class SettingsScreen:
    def __init__(self, app, user_role, backend):
        self.app = app
        self.user_role = user_role
        self.backend = backend

        # Settings Frame
        self.settings_frame = customtkinter.CTkFrame(self.app, corner_radius=15, border_width=3, border_color="#1abc9c")
        self.settings_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Settings Header
        settings_label = customtkinter.CTkLabel(self.settings_frame, text="Settings", font=("Arial", 24, "bold"), text_color="#34495e")
        settings_label.pack(pady=20)

        # Theme Change Dropdown
        customtkinter.CTkLabel(self.settings_frame, text="Select Theme:", text_color="#34495e").pack(pady=5)
        theme_option_menu = customtkinter.CTkOptionMenu(
            self.settings_frame, values=["Light", "Dark", "Blue"], command=self.change_theme,
            fg_color="#1abc9c", button_color="#1abc9c", text_color="#ffffff"
        )
        theme_option_menu.pack(pady=10)

        # Fullscreen Toggle Button
        fullscreen_button = customtkinter.CTkButton(
            self.settings_frame, text="Toggle Fullscreen", command=self.toggle_fullscreen, width=160, height=50,
            corner_radius=10, fg_color="#1abc9c", hover_color="#16a085", text_color="#ffffff"
        )
        fullscreen_button.pack(pady=10)

        # Upload Profile Photo Button
        upload_photo_button = customtkinter.CTkButton(
            self.settings_frame, text="Upload Profile Photo", command=self.upload_photo, width=160, height=50,
            corner_radius=10, fg_color="#1abc9c", hover_color="#16a085", text_color="#ffffff"
        )
        upload_photo_button.pack(pady=20)

        # Terminate User Section (Only for Supervisors)
        if self.user_role == 'Supervisor':
            terminate_button = customtkinter.CTkButton(
                self.settings_frame, text="Terminate User", command=self.show_terminate_screen, width=160, height=50,
                corner_radius=10, fg_color="#FF4C4C", hover_color="#FF1C1C", text_color="#ffffff"
            )
            terminate_button.pack(pady=10, fill="x")

        # Log Out Button with Audio
        logout_button = customtkinter.CTkButton(
            self.settings_frame, text="Log Out", command=self.logout_with_audio, width=160, height=50,
            corner_radius=10, fg_color="#FF4C4C", hover_color="#FF1C1C", text_color="#ffffff"
        )
        logout_button.pack(pady=10, fill="x")

        # Close App Button with Audio
        close_app_button = customtkinter.CTkButton(
            self.settings_frame, text="Close App", command=self.close_app_with_audio, width=160, height=50,
            corner_radius=10, fg_color="#FF4C4C", hover_color="#FF1C1C", text_color="#ffffff"
        )
        close_app_button.pack(pady=10, fill="x")

    def change_theme(self, theme_name):
        # Apply the selected theme
        customtkinter.set_appearance_mode(theme_name.lower())

    def toggle_fullscreen(self):
        self.app.is_full_screen = not self.app.is_full_screen
        self.app.attributes("-fullscreen", self.app.is_full_screen)

    def upload_photo(self):
        """Upload a profile photo and save it for the current user."""
        file_path = filedialog.askopenfilename(
            title="Select a Profile Photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            try:
                # Create 'images' directory if it doesn't exist
                if not os.path.exists("../static/images"):
                    os.makedirs("../static/images")

                # Copy the selected photo to the 'images' directory with a specific naming convention
                dest_path = os.path.join("../static/images", f"{self.app.current_user}_profile_photo.png")
                shutil.copy(file_path, dest_path)
                messagebox.showinfo("Upload Photo", f"Photo successfully uploaded for {self.app.current_user}.")
            except Exception as e:
                messagebox.showerror("Upload Error", f"Failed to upload photo: {e}")
        else:
            messagebox.showwarning("Upload Photo", "No photo was selected.")

    def show_terminate_screen(self):
        # Create the terminate user screen
        terminate_window = customtkinter.CTkToplevel(self.app)
        terminate_window.title("Terminate User")
        terminate_window.geometry("400x400")

        # Header
        terminate_label = customtkinter.CTkLabel(terminate_window, text="Terminate User", font=("Arial", 20, "bold"),
                                                 fg_color="#FF4C4C", text_color="#ffffff")
        terminate_label.pack(pady=20)

        # List of users to select from
        user_list = self.backend.get_all_users()  # Get all users from backend
        self.selected_user = customtkinter.StringVar()
        self
