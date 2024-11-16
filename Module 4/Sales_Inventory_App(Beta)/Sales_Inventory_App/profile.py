import customtkinter
import os
from PIL import Image, ImageTk

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
        image_path = os.path.join("images", f"{self.username}.png")
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

