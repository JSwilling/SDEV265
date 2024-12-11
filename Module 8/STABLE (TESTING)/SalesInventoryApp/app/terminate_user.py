import customtkinter
from tkinter import messagebox

class TerminateUserScreen:
    def __init__(self, app, backend):
        self.app = app
        self.backend = backend

        # Create the terminate user screen as a Toplevel window
        self.terminate_window = customtkinter.CTkToplevel(app)
        self.terminate_window.title("Terminate User")
        self.terminate_window.geometry("400x400")
        self.terminate_window.grab_set()  # Keep window in focus until closed

        # Title
        title_label = customtkinter.CTkLabel(self.terminate_window, text="Terminate User", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        # List of users
        self.users = self.backend.get_all_users()

        if not self.users:
            # If no users are available, display a message
            no_users_label = customtkinter.CTkLabel(self.terminate_window, text="No users available.")
            no_users_label.pack(pady=20)
            return

        # User selection dropdown
        self.selected_user = customtkinter.StringVar()
        self.user_dropdown = customtkinter.CTkOptionMenu(self.terminate_window, variable=self.selected_user, values=self.users)
        self.user_dropdown.pack(pady=20)

        # Terminate button
        terminate_button = customtkinter.CTkButton(self.terminate_window, text="Terminate", command=self.terminate_user, fg_color="red", hover_color="darkred")
        terminate_button.pack(pady=20)

    def terminate_user(self):
        # Confirmation prompt
        if not self.selected_user.get():
            messagebox.showwarning("Error", "Please select a user.")
            return

        confirm = messagebox.askyesno("Confirm Termination", f"Are you sure you want to terminate the user '{self.selected_user.get()}'?")
        if confirm:
            self.backend.delete_user(self.selected_user.get())
            messagebox.showinfo("Terminated", f"User '{self.selected_user.get()}' has been terminated.")
            self.terminate_window.destroy()
