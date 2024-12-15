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
        self.settings_frame = customtkinter.CTkFrame(self.app, corner_radius=15, border_width=3, border_color="#1abc9c")
        self.settings_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Settings Header
        settings_label = customtkinter.CTkLabel(self.settings_frame, text="Settings", font=("Arial", 24, "bold"), text_color="#34495e")
        settings_label.pack(pady=20)

        # Theme Change Dropdown
        customtkinter.CTkLabel(self.settings_frame, text="Select Theme:", text_color="#34495e").pack(pady=5)
        theme_option_menu = customtkinter.CTkOptionMenu(
            self.settings_frame, values=["Light", "Dark"], command=self.change_theme,
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
        """Change the theme of the application."""
        if theme_name == "Light":
            customtkinter.set_appearance_mode("light")
        elif theme_name == "Dark":
            customtkinter.set_appearance_mode("dark")

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        self.app.is_full_screen = not self.app.is_full_screen
        if self.app.is_full_screen:
            self.app.attributes("-fullscreen", True)
        else:
            self.app.attributes("-fullscreen", False)

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
        self.user_combobox = ttk.Combobox(terminate_window, textvariable=self.selected_user, values=user_list, state="readonly")
        self.user_combobox.pack(pady=10)

        # Submit Button to Confirm Termination
        terminate_submit_button = customtkinter.CTkButton(
            terminate_window, text="Submit", command=self.confirm_termination, fg_color="#FF4C4C", hover_color="#FF1C1C",
            text_color="#ffffff"
        )
        terminate_submit_button.pack(pady=20)

    def confirm_termination(self):
        """Confirm and terminate the selected user."""
        selected_user = self.selected_user.get()
        if not selected_user:
            messagebox.showwarning("Selection Error", "Please select a user to terminate.")
            return

        response = messagebox.askyesno("Confirm Termination", f"Are you sure you want to terminate user: {selected_user}? This action cannot be undone.")
        if response:
            self.backend.delete_user(selected_user)
            messagebox.showinfo("Success", f"User '{selected_user}' has been terminated.")
            self.user_combobox['values'] = self.backend.get_all_users()  # Refresh user list after deletion

    def logout_with_audio(self):
        """Play audio when logging out and then show login screen."""
        try:
            pygame.mixer.music.load('logout.mp3')  # Ensure the path to the audio file is correct
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing logout audio: {e}")
        finally:
            self.app.show_login_screen()

    def close_app_with_audio(self):
        """Play audio when closing the app and then close."""
        try:
            pygame.mixer.music.load('close_app.mp3')  # Ensure the path to the audio file is correct
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing close app audio: {e}")
        finally:
            self.app.quit()
