import customtkinter
import os
from PIL import Image, ImageTk
import shutil
from tkinter import filedialog, messagebox

class ProfileScreen:
    def __init__(self, app, username, role):
        self.app = app
        self.username = username
        self.role = role

        # Profile Frame with updated theme colors and border
        self.profile_frame = customtkinter.CTkFrame(self.app, corner_radius=15, border_width=3, border_color="#1abc9c")
        self.profile_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Main Content Frame
        main_content_frame = customtkinter.CTkFrame(self.profile_frame, corner_radius=10, fg_color="#f7f9fc")
        main_content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Profile Picture Section
        image_path = self.get_profile_photo_path()
        if os.path.exists(image_path):
            image = Image.open(image_path).resize((200, 200))
            self.profile_photo = ImageTk.PhotoImage(image)
            profile_photo_label = customtkinter.CTkLabel(main_content_frame, image=self.profile_photo, fg_color="transparent")
        else:
            profile_photo_label = customtkinter.CTkLabel(main_content_frame, text="No Profile Photo", width=200, height=200, corner_radius=15, fg_color="#dfe6e9")
        profile_photo_label.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        # User Information Section
        user_info_frame = customtkinter.CTkFrame(main_content_frame, corner_radius=10, fg_color="transparent")
        user_info_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        username_label = customtkinter.CTkLabel(user_info_frame, text=f"Username: {self.username}", font=("Arial", 20, "bold"), text_color="#34495e")
        username_label.pack(anchor="w", pady=5)

        role_label = customtkinter.CTkLabel(user_info_frame, text=f"Role: {self.role}", font=("Arial", 16), text_color="#34495e")
        role_label.pack(anchor="w", pady=5)

        # Additional Info Section (Simulating Social Media Layout)
        additional_info_frame = customtkinter.CTkFrame(main_content_frame, corner_radius=10, fg_color="transparent")
        additional_info_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="n")

        additional_info_label = customtkinter.CTkLabel(additional_info_frame, text="Recent Activity", font=("Arial", 18, "bold"), text_color="#34495e")
        additional_info_label.pack(anchor="w", pady=10)

        # Example of recent activities (Placeholder)
        for i in range(5):
            activity_label = customtkinter.CTkLabel(additional_info_frame, text=f"Activity {i+1}: Placeholder text for recent activity.", font=("Arial", 14), text_color="#34495e")
            activity_label.pack(anchor="w", pady=2)

        # Back button - updated to match navigation theme
        back_button = customtkinter.CTkButton(
            self.profile_frame, text="Back", command=self.app.show_dashboard_screen,
            width=160, height=50, corner_radius=10,
            fg_color="#1abc9c", hover_color="#16a085", text_color="#ffffff"
        )
        back_button.pack(pady=20)

    def get_profile_photo_path(self):
        # Path where the profile photo will be saved and loaded from
        return os.path.join("images", f"{self.username}_profile_photo.png")

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
                if not os.path.exists("images"):
                    os.makedirs("images")

                # Copy the selected photo to the 'images' directory with a specific naming convention
                dest_path = os.path.join("images", f"{self.app.current_user}_profile_photo.png")
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
