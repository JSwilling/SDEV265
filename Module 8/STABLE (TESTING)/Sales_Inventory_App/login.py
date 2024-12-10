import customtkinter
from tkinter import messagebox
from PIL import Image
import sqlite3
import bcrypt  # For password hashing
import base64  # For encoding and decoding hashed passwords


class LoginScreen:
    def __init__(self, app, login_success_callback):
        self.app = app
        self.login_success_callback = login_success_callback

        # Set up the appearance mode and color theme
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        self.app.configure(bg="#ffffff")  # Set consistent app background color

        # Make the application frameless
        self.app.overrideredirect(True)

        # Main frame for the login screen - centralized card design
        self.login_frame = customtkinter.CTkFrame(
            self.app, corner_radius=15, width=400, height=650,
            fg_color="#ffffff", border_width=3, border_color="#c0392b"
        )
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.login_frame.pack_propagate(False)  # Prevent resizing based on child widgets

        # Placeholder for company logo - adjust as needed
        try:
            self.logo_image = Image.open(r"Module 8\STABLE (TESTING)\Sales_Inventory_App\placeholder_logo.png")  # Ensure the image exists
            self.logo_ctk_image = customtkinter.CTkImage(self.logo_image, size=(200, 200))
            logo_label = customtkinter.CTkLabel(
                self.login_frame, image=self.logo_ctk_image, text="", fg_color="#ffffff"
            )
            logo_label.pack(pady=(20, 0))
        except Exception as e:
            print(f"Error loading logo image: {e}")

        # Username Entry
        customtkinter.CTkLabel(
            self.login_frame, text="Username", font=("Verdana", 16),
            fg_color="#ffffff", text_color="#c0392b"
        ).pack(pady=(20, 5))

        self.username_entry = customtkinter.CTkEntry(
            self.login_frame, width=300, height=40, corner_radius=10,
            placeholder_text="Enter your username", fg_color="#ffffff", text_color="#000000"
        )
        self.username_entry.pack(pady=5)

        # Password Entry
        customtkinter.CTkLabel(
            self.login_frame, text="Password", font=("Verdana", 16),
            fg_color="#ffffff", text_color="#c0392b"
        ).pack(pady=(20, 5))

        self.password_entry = customtkinter.CTkEntry(
            self.login_frame, show="*", width=300, height=40, corner_radius=10,
            placeholder_text="Enter your password", fg_color="#ffffff", text_color="#000000"
        )
        self.password_entry.pack(pady=5)

        # Login and Register Buttons
        button_frame = customtkinter.CTkFrame(self.login_frame, fg_color="transparent")
        button_frame.pack(pady=(30, 10))

        register_button = customtkinter.CTkButton(
            button_frame, text="Register", command=self.show_register_window, width=120, height=40, corner_radius=10,
            fg_color="#c0392b", hover_color="#e74c3c", text_color="#ffffff"
        )
        register_button.grid(row=0, column=0, padx=6)

        login_button = customtkinter.CTkButton(
            button_frame, text="Sign In", command=self.login_action, width=140, height=40, corner_radius=10,
            fg_color="#c0392b", hover_color="#e74c3c", text_color="#ffffff"
        )
        login_button.grid(row=0, column=1, padx=6)

        # Help link for signing in
        help_button = customtkinter.CTkButton(
            self.login_frame, text="Help signing in?", command=self.show_help_window,
            fg_color="transparent", text_color="#c0392b", hover=False, font=("Verdana", 12)
        )
        help_button.pack(pady=10)

        # Custom Close Button to close the frameless window
        close_button = customtkinter.CTkButton(
            self.login_frame, text="X", command=self.close_app, width=40, height=40, corner_radius=20,
            fg_color="#e74c3c", hover_color="#c0392b", text_color="#ffffff"
        )
        close_button.place(relx=0.98, rely=0.02, anchor="ne")

        # Optional: Bind movement of the window (click and drag) to the entire frame
        self.login_frame.bind("<B1-Motion>", self.move_window)
        self.login_frame.bind("<Button-1>", self.start_move)

        # Initialize fade-in effect
        self.fade_in_effect()

    def fade_in_effect(self, alpha=0):
        """Gradually increases window opacity from 0 to 1"""
        if alpha < 1.0:
            alpha += 0.05  # Adjust the increment for faster fade-in
            self.app.wm_attributes("-alpha", alpha)
            self.app.after(50, lambda: self.fade_in_effect(alpha))
        else:
            self.app.wm_attributes("-alpha", 1.0)  # Ensure full opacity at the end

    def close_app(self):
        self.app.destroy()

    def start_move(self, event):
        # Record the starting position for movement
        self._offsetx = event.x
        self._offsety = event.y

    def move_window(self, event):
        # Calculate the new position based on pointer movement
        x = self.app.winfo_pointerx() - self._offsetx
        y = self.app.winfo_pointery() - self._offsety
        self.app.geometry(f"+{x}+{y}")

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return
        conn = sqlite3.connect(r'Module 8\STABLE (TESTING)\Sales_Inventory_App\Sales_Inventory.db')  # Connect to the SQLite database
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_hashed_password_base64 = result[0]  # Base64-encoded hashed password
            role = result[1]

            # Decode the base64-encoded hashed password back to bytes
            stored_hashed_password = base64.b64decode(stored_hashed_password_base64.encode('utf-8'))

            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                self.login_success_callback(username, role)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_register_window(self):
        if not hasattr(self, 'register_window') or not self.register_window.winfo_exists():
            self.register_window = RegisterWindow(self.app)
        else:
            self.register_window.lift()

    def show_help_window(self):
        # Implement help window functionality here
        messagebox.showinfo("Help", "Please contact support for assistance.")

    def show_register_window(self):
        if not hasattr(self, 'register_window') or not self.register_window.winfo_exists():
            self.register_window = RegisterWindow(self.app)
        else:
            self.register_window.lift()

    def show_help_window(self):
        # Implement help window functionality here
        messagebox.showinfo("Help", "Please contact support for assistance.")


class RegisterWindow(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Register")
        self.geometry("500x600")
        self.resizable(False, False)
        self.configure(bg="#ffffff")

        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) // 2
        self.geometry(f"+{x}+{y}")

        # Registration form
        self.create_registration_form()

    def create_registration_form(self):
        self.register_frame = customtkinter.CTkFrame(self, corner_radius=15, fg_color="#ffffff")
        self.register_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.register_frame.pack_propagate(False)

        # Title
        title_label = customtkinter.CTkLabel(
            self.register_frame,
            text="Create an Account",
            font=("Verdana", 24, "bold"),
            text_color="#c0392b"
        )
        title_label.pack(pady=20)

        # Username Entry
        customtkinter.CTkLabel(
            self.register_frame,
            text="Username",
            font=("Verdana", 16),
            text_color="#c0392b"
        ).pack(pady=(10, 5))

        self.username_entry = customtkinter.CTkEntry(
            self.register_frame,
            width=300,
            height=40,
            corner_radius=10,
            placeholder_text="Enter a username",
            fg_color="#ffffff",
            text_color="#000000"
        )
        self.username_entry.pack(pady=5)

        # Password Entry
        customtkinter.CTkLabel(
            self.register_frame,
            text="Password",
            font=("Verdana", 16),
            text_color="#c0392b"
        ).pack(pady=(10, 5))

        self.password_entry = customtkinter.CTkEntry(
            self.register_frame,
            show="*",
            width=300,
            height=40,
            corner_radius=10,
            placeholder_text="Enter a password",
            fg_color="#ffffff",
            text_color="#000000"
        )
        self.password_entry.pack(pady=5)

        # Confirm Password Entry
        customtkinter.CTkLabel(
            self.register_frame,
            text="Confirm Password",
            font=("Verdana", 16),
            text_color="#c0392b"
        ).pack(pady=(10, 5))

        self.confirm_password_entry = customtkinter.CTkEntry(
            self.register_frame,
            show="*",
            width=300,
            height=40,
            corner_radius=10,
            placeholder_text="Confirm your password",
            fg_color="#ffffff",
            text_color="#000000"
        )
        self.confirm_password_entry.pack(pady=5)

        # Role Selection
        customtkinter.CTkLabel(
            self.register_frame,
            text="Role",
            font=("Verdana", 16),
            text_color="#c0392b"
        ).pack(pady=(10, 5))

        self.role_optionmenu = customtkinter.CTkOptionMenu(
            self.register_frame,
            values=["Employee", "Supervisor", "Salesperson"],
            width=300,
            height=40,
            corner_radius=10,
            button_color="#c0392b",
            button_hover_color="#e74c3c",
            text_color="#000000"
        )
        self.role_optionmenu.set("User")  # Default value
        self.role_optionmenu.pack(pady=5)

        # Register Button
        register_button = customtkinter.CTkButton(
            self.register_frame,
            text="Register",
            command=self.register_user,
            width=200,
            height=40,
            corner_radius=10,
            fg_color="#c0392b",
            hover_color="#e74c3c",
            text_color="#ffffff"
        )
        register_button.pack(pady=30)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        role = self.role_optionmenu.get()

        if not username or not password or not confirm_password:
            messagebox.showwarning("Input Error", "Please fill out all fields.")
            return

        if password != confirm_password:
            messagebox.showwarning("Password Mismatch", "Passwords do not match.")
            return

        # Validate password complexity (optional)
        if len(password) < 6:
            messagebox.showwarning("Weak Password", "Password must be at least 6 characters long.")
            return

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Encode the hashed password using Base64
        hashed_password_base64 = base64.b64encode(hashed_password).decode('utf-8')

        # Save the new user to the database
        conn = sqlite3.connect(r'Module 8\STABLE (TESTING)\Sales_Inventory_App\Sales_Inventory.db')  # Adjust the path if needed
        cursor = conn.cursor()

        # Create the users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            messagebox.showwarning("Username Taken", "This username is already taken.")
            conn.close()
            return

        # Insert the new user
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password_base64, role)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Registration Successful", "Your account has been created.")
        self.destroy()  # Close the registration window

    def lift(self):
        self.attributes('-topmost', True)
        self.attributes('-topmost', False)
