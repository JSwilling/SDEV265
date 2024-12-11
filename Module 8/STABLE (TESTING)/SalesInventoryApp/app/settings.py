import customtkinter
from tkinter import messagebox, ttk, filedialog
import pygame
import os
import shutil

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

        # Notifications Section
        self.add_section_label("Notifications")
        self.notification_var = customtkinter.StringVar(value="Enabled")
        notification_toggle = customtkinter.CTkOptionMenu(
            self.settings_frame, values=["Enabled", "Disabled"], variable=self.notification_var,
            fg_color="#E74C3C", button_color="#C0392B", text_color="#FFFFFF"
        )
        notification_toggle.pack(pady=10)

        # Privacy Settings Section
        self.add_section_label("Privacy Settings")
        privacy_toggle = customtkinter.CTkSwitch(
            self.settings_frame, text="Enable Two-Factor Authentication", onvalue="Enabled", offvalue="Disabled",
            fg_color="#9B59B6", progress_color="#8E44AD"
        )
        privacy_toggle.pack(pady=10)


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

    def add_section_label(self, text):
        """Helper to add section headers."""
        section_label = customtkinter.CTkLabel(
            self.settings_frame, text=text, font=("Arial", 18, "bold"), text_color="#34495E"
        )
        section_label.pack(pady=15)

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
