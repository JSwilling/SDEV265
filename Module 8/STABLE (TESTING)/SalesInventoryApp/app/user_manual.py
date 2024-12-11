import tkinter as tk
from tkinter import ttk
import customtkinter

class UserManual:
    def __init__(self, parent):
        # Create a separate Toplevel window for the user manual
        self.window = tk.Toplevel(parent)
        self.window.title("User Manual")  # Add a title for clarity
        self.window.geometry("700x800")  # Larger dimensions for better readability
        self.window.configure(bg="white")  # White background
        self.window.resizable(True, True)  # Make the window resizable

        # Enable dragging the window
        self.window.bind("<ButtonPress-1>", self.start_drag)
        self.window.bind("<B1-Motion>", self.drag_window)

        # Outer container with curved borders
        self.container = customtkinter.CTkFrame(
            self.window,
            corner_radius=15,
            fg_color="white"
        )
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        self.header = customtkinter.CTkLabel(
            self.container,
            text="\ud83d\udcd8 User Manual",
            font=("Arial", 20, "bold"),
            text_color="black"
        )
        self.header.pack(pady=(10, 20))

        # Scrollable content area
        self.scroll_canvas = tk.Canvas(self.container, bg="white", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.container,
            orient="vertical",
            command=self.scroll_canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame = customtkinter.CTkFrame(self.scroll_canvas, fg_color="white")
        self.scrollable_window = self.scroll_canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw"
        )

        # Populate content
        self.populate_content()

        # Update scrollable region
        self.scroll_frame.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

        self.scroll_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def populate_content(self):
        sections = [
            ("Introduction", "Welcome to the Sales Inventory App! \nThis manual will guide you through the \nfeatures and functionality of the application."),
            ("Features", "\n\n- \ud83d\udce6 Manage Inventory: Organize and track your inventory\n - \ud83d\udcca Generate Reports: Create detailed sales and \ninventory reports.\n- \u2692\ufe0f Configure Settings: Customize your experience.\n- \ud83d\udc65 Manage Users: Add, edit, or remove users."),
            ("How to Use", "\n1. Log in using your credentials.\n2. Use the navigation pane to switch between features.\n3. Follow on-screen prompts to manage \ninventory, generate reports, or modify settings."),
            ("Help with Logging In", "If you have trouble logging in:\n- Ensure your username and password are correct.\n- Click on 'Forgot Password' to reset your credentials.\n- Contact support if you encounter persistent issues."),
            ("Contact Support", "\ud83d\udcde Phone: +123 456 7890\n\ud83d\udce7 Email: support@example.com\n\ud83c\udf10 Website: www.salesinventoryapp.com")
        ]

        for title, content in sections:
            title_label = customtkinter.CTkLabel(
                self.scroll_frame,
                text=title,
                font=("Arial", 18, "bold"),
                text_color="black",
                wraplength=660  # Ensure text wraps within the container
            )
            title_label.pack(pady=(10, 5), anchor="w")

            content_label = customtkinter.CTkLabel(
                self.scroll_frame,
                text=content,
                font=("Arial", 14),
                text_color="gray",
                wraplength=660
            )
            content_label.pack(pady=(0, 10), anchor="w")

        # Centered Close Button
        close_button = customtkinter.CTkButton(
            self.scroll_frame,
            text="Close Manual",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            text_color="white",
            command=self.window.destroy
        )
        close_button.pack(pady=20, anchor="s")

    def start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def drag_window(self, event):
        x = self.window.winfo_x() - self.start_x + event.x
        y = self.window.winfo_y() - self.start_y + event.y
        self.window.geometry(f"+{x}+{y}")

    def on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(-1 * (event.delta // 120), "units")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    user_manual = UserManual(root)
    root.mainloop()
