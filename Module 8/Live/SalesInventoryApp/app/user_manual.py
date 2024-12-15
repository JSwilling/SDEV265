import tkinter as tk
from tkinter import ttk
import customtkinter

class UserManual:
    def __init__(self, parent):
        # Create a separate Toplevel window for the user manual
        self.window = tk.Toplevel(parent)
        self.window.title("User Manual")
        self.window.geometry("700x800")
        self.window.configure(bg="#ffffff")  # White background
        self.window.resizable(False, False)  # Disable resizing
        self.window.overrideredirect(True)  # Frameless window

        # Enable dragging the window
        self.window.bind("<ButtonPress-1>", self.start_drag)
        self.window.bind("<B1-Motion>", self.drag_window)

        # Outer container
        self.container = customtkinter.CTkFrame(
            self.window,
            corner_radius=15,
            fg_color="#ffffff"
        )
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        self.create_header()

        # Scrollable content area
        self.scroll_canvas = tk.Canvas(self.container, bg="#ffffff", highlightthickness=0)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.container,
            orient="vertical",
            command=self.scroll_canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame = customtkinter.CTkFrame(self.scroll_canvas, fg_color="#ffffff")
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

    def create_header(self):
        """Create the header with a close button."""
        header_frame = customtkinter.CTkFrame(self.container, fg_color="#C0392B")
        header_frame.pack(fill="x", pady=(0, 10))

        header_label = customtkinter.CTkLabel(
            header_frame,
            text="\ud83d\udcd8 User Manual",
            font=("Arial", 20, "bold"),
            text_color="#ffffff"
        )
        header_label.pack(side="left", padx=10)

        close_button = customtkinter.CTkButton(
            header_frame,
            text="X",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            text_color="white",
            command=self.window.destroy,
            width=40,
            height=40,
            corner_radius=20
        )
        close_button.pack(side="right", padx=10)

    def populate_content(self):
        """Add content sections to the manual."""
        sections = [
            ("📖 Introduction", "Welcome to the Sales Inventory App!\n This manual will guide you through the\n features and functionality of the application."),
            ("✨ Features", "- 📦 **Manage Inventory**: Organize and\n track your inventory.\n- 📊 **Generate Reports**: Create detailed\n sales and inventory reports.\n- ⚙️ **Configure Settings**: Customize your experience.\n- 👥 **Manage Users**: Add, edit, or remove users."),
            ("🔑 Default Login", "The default login for the application is:\n- **Username**: Admin\n- **Password**: TESTING"),
            ("👩‍💼 Role of Supervisors", "Supervisors play a critical role\n in managing the system:\n- Assign roles to users.\n- Ensure proper user \naccess control.\n- Perform critical actions such as \nclearing the database or managing permissions."),
            ("📋 How to Use", "1. Log in using your credentials.\n2. Use the navigation pane to switch between features.\n3. Follow on-screen prompts to manage\n inventory, generate reports, or modify settings."),
            ("❓ Help with Logging In", "If you have trouble logging in:\n- Ensure your username and password are correct.\n- Contact support if you encounter persistent issues."),
            ("📞 Contact Support", "☎️ Phone: +123 456 7890\n📧 Email: support@example.com\n🌐 Website: www.salesinventoryapp.com")
        ]

        for title, content in sections:
            title_label = customtkinter.CTkLabel(
                self.scroll_frame,
                text=title,
                font=("Arial", 18, "bold"),
                text_color="#C0392B",
                wraplength=660  # Dynamically wrap text based on the frame width
            )
            title_label.pack(pady=(10, 5), anchor="w")

            content_label = customtkinter.CTkLabel(
                self.scroll_frame,
                text=content,
                font=("Arial", 14),
                text_color="gray",
                wraplength=660  # Dynamically wrap text based on the frame width
            )
            content_label.pack(pady=(0, 10), anchor="w")

    def start_drag(self, event):
        """Start dragging the window."""
        self.start_x = event.x
        self.start_y = event.y

    def drag_window(self, event):
        """Drag the window to a new position."""
        x = self.window.winfo_x() - self.start_x + event.x
        y = self.window.winfo_y() - self.start_y + event.y
        self.window.geometry(f"+{x}+{y}")

    def on_mousewheel(self, event):
        """Scroll the canvas on mouse wheel movement."""
        self.scroll_canvas.yview_scroll(-1 * (event.delta // 120), "units")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    user_manual = UserManual(root)
    root.mainloop()