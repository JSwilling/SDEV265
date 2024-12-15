import tkinter as tk
import tkinter.ttk as ttk
import customtkinter
import pygame
import sqlite3
import os
import shutil
import time
import random
import numpy as np
import ttkbootstrap as ttkb
from tkinter import StringVar, filedialog
from login import LoginScreen
from navigation import CreateNavigationPane  # Use the updated navigation class
from report import GenerateReportScreen
from dashboard import DashboardScreen
from inventory_management import ManageInventoryScreen
from settings import SettingsScreen
from profile import ProfileScreen
from terminate_user import TerminateUserScreen
from backend import Backend
from report_generator import ReportGenerator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from inventory_management import ManageStaffScreen
import threading

# Initialize Pygame mixer at the start of the script
pygame.mixer.init()

customtkinter.set_appearance_mode("Light")  # or "Dark"
customtkinter.set_default_color_theme("blue")  # or any other theme

# Initialize backend
backend = Backend()
backend.create_database()


class ManageStaffScreen:
    def __init__(self, app, backend, user_role):
        self.app = app
        self.backend = backend
        self.user_role = user_role
        self.setup_ui()

    def setup_ui(self):
        # Main Frame
        self.main_frame = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color=self.get_background_color())
        self.main_frame.pack(fill="both", expand=True)

        # Create Notebook for Tabs with enhanced styling
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[10, 10], font=('Arial', 14, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#1ABC9C')], foreground=[('selected', 'white')])

        self.tab_control = ttk.Notebook(self.main_frame, style='TNotebook')
        self.tab_control.pack(expand=1, fill="both", padx=20, pady=20)

        # Define Tabs
        self.employees_tab = customtkinter.CTkFrame(self.tab_control, corner_radius=15, fg_color=self.get_background_color())
        self.manage_tab = customtkinter.CTkFrame(self.tab_control, corner_radius=15, fg_color=self.get_background_color())

        # Add Tabs to Notebook
        self.tab_control.add(self.employees_tab, text='Employees')
        self.setup_employees_tab()

        self.tab_control.add(self.manage_tab, text='Manage')
        self.setup_manage_tab()

    def setup_employees_tab(self):
        title_color = '#FFFFFF' if self.is_dark_mode() else '#2C3E50'
        title_label = customtkinter.CTkLabel(self.employees_tab, text="Employees", font=("Arial", 24, "bold"), text_color=title_color)
        title_label.pack(pady=20)

        # Placeholder for Employee Table (TreeView)
        columns = ("Employee ID", "Name", "Position", "Team", "Office", "Country")
        self.employee_table = ttk.Treeview(self.employees_tab, columns=columns, show="headings", height=10)
        for col in columns:
            self.employee_table.heading(col, text=col)
            self.employee_table.column(col, width=150, anchor="center")
        self.employee_table.pack(pady=10, padx=10, fill="both", expand=True)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.employees_tab, orient="vertical", command=self.employee_table.yview)
        self.employee_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Load employee data
        self.load_employees()

        # Bind employee selection to open profile
        self.employee_table.bind("<<TreeviewSelect>>", self.show_employee_profile)

    def setup_manage_tab(self):
        title_color = '#FFFFFF' if self.is_dark_mode() else '#2C3E50'
        title_label = customtkinter.CTkLabel(self.manage_tab, text="Manage Staff", font=("Arial", 24, "bold"), text_color=title_color)
        title_label.pack(pady=20)

        # Terminate User Button
        terminate_user_button = customtkinter.CTkButton(
            self.manage_tab, text="Terminate User", command=self.terminate_user, fg_color="#FF4C4C", hover_color="#FF1C1C", text_color="#ffffff"
        )
        terminate_user_button.pack(pady=10)

        # Placeholder for other management options
        # You can add additional buttons and forms here to manage staff members

    def load_employees(self):
        # Placeholder function to load employee data - Replace this with actual backend call
        sample_employees = [
            ("E001", "John Doe", "UX Designer", "Design", "London", "United Kingdom"),
            ("E002", "Jane Smith", "Software Engineer", "Development", "New York", "United States"),
        ]
        for employee in sample_employees:
            self.employee_table.insert("", "end", values=employee)

    def show_employee_profile(self, event=None):
        # Open a popup to show employee details
        selected_item = self.employee_table.selection()
        if selected_item:
            employee_data = self.employee_table.item(selected_item, 'values')
            profile_window = customtkinter.CTkToplevel(self.app)
            profile_window.title("Employee Profile")
            profile_window.geometry("400x400")

            # Header
            profile_label = customtkinter.CTkLabel(profile_window, text="Employee Profile", font=("Arial", 20, "bold"), fg_color="#1ABC9C", text_color="#ffffff")
            profile_label.pack(pady=20)

            # Display Employee Details
            details_text = f"Employee ID: {employee_data[0]}\nName: {employee_data[1]}\nPosition: {employee_data[2]}\nTeam: {employee_data[3]}\nOffice: {employee_data[4]}\nCountry: {employee_data[5]}"
            details_label = customtkinter.CTkLabel(profile_window, text=details_text, font=("Arial", 16), text_color="#34495e", wraplength=350)
            details_label.pack(pady=20, padx=10)

            # Back button
            back_button = customtkinter.CTkButton(profile_window, text="Close", command=profile_window.destroy, width=160, height=50, corner_radius=10, fg_color="#1abc9c", hover_color="#16a085", text_color="#ffffff")
            back_button.pack(pady=20)

    def terminate_user(self):
        # Placeholder function for terminating a user - Implement backend call here
        selected_item = self.employee_table.selection()
        if selected_item:
            employee_data = self.employee_table.item(selected_item, 'values')
            confirm = tk.messagebox.askyesno("Confirm Termination", f"Are you sure you want to terminate {employee_data[1]}?")
            if confirm:
                # Here you would call your backend to terminate the user
                tk.messagebox.showinfo("User Terminated", f"{employee_data[1]} has been terminated successfully.")

    def is_dark_mode(self):
        return customtkinter.get_appearance_mode() == "Dark"

    def get_background_color(self):
        return '#2C3E50' if self.is_dark_mode() else 'white'

def show_manage_staff_screen(app, backend, user_role):
    ManageStaffScreen(app, backend, user_role)



class GenerateReportPopup(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Generate Sales Report")
        self.geometry("600x500")
        self.parent = parent

        # Fetch item IDs from the database
        self.item_ids = self.get_item_ids()

        # Create dropdown menu
        self.item_id_var = tk.StringVar(value=self.item_ids[0])
        self.dropdown = customtkinter.CTkOptionMenu(
            self,
            values=self.item_ids,
            variable=self.item_id_var
        )
        self.dropdown.pack(pady=20)

        # Create button to generate report
        self.generate_button = customtkinter.CTkButton(
            self,
            text="Generate Report",
            command=self.generate_report
        )
        self.generate_button.pack(pady=10)

        # Placeholder for the plot
        self.canvas = None

    def get_item_ids(self):
        # Connect to the database and fetch all item IDs
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT item_id FROM items")
        items = cursor.fetchall()
        conn.close()
        # Return a list of item IDs as strings
        return [str(item[0]) for item in items]

    def generate_report(self):
        # Get selected item ID
        selected_item_id = self.item_id_var.get()
        # Start a new thread to generate the report
        threading.Thread(target=self.create_live_plot, args=(selected_item_id,)).start()

    def create_live_plot(self, item_id):
        # Fetch sales data for the selected item from the database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, quantity FROM sales
            WHERE item_id = ?
            ORDER BY date ASC
        ''', (item_id,))
        data = cursor.fetchall()
        conn.close()

        if not data:
            print("No sales data available for this item.")
            return

        dates = [row[0] for row in data]
        quantities = [row[1] for row in data]

        # Create the plot
        plt.style.use('seaborn-darkgrid')
        fig, ax = plt.subplots(figsize=(6, 4))
        line, = ax.plot_date(dates, quantities, '-o')

        ax.set_title(f"Sales Data for Item ID {item_id}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Quantity Sold")

        # Embed the plot in the Tkinter window
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=20)

        # Optionally, add animation
        # For simplicity, let's simulate live data updates
        for _ in range(5):  # Simulate 5 updates
            quantities = [q + 1 for q in quantities]  # Simulate data change
            line.set_ydata(quantities)
            self.canvas.draw()
            plt.pause(1)  # Pause for 1 second


class InventoryApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title("Inventory Management System")
        self.resizable(False, False)  # Disable maximize button on the login screen
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        self.current_user = None
        self.current_user_role = None
        self.nav_frame = None
        self.is_full_screen = False

        # Play startup jingle
        self.play_audio("startup.mp3")

        self.show_login_screen()

        # Apply the border with glow effect
        self.configure(bg="#1abc9c")  # Border color similar to login screen
        self.update_idletasks()

        # Set the app to be on top at startup
        self.lift()  # Raise the window
        self.attributes('-topmost', True)  # Ensure the window stays on top
        self.after(1000, lambda: self.attributes('-topmost', False))  # Remove the "always on top" after 1 second

    def play_audio(self, file_path):
        """Play an audio file using pygame."""
        try:
            pygame.mixer.music.load(r'Module 6\\Updated App M07\\Sales_Inventory_App\\test.mp3')
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing audio file: {e}")

    def on_close(self):
        # Play logout sound before closing
        pygame.mixer.music.load(r'Module 6\\Updated App M07\\Sales_Inventory_App\\log_out_sound.mp3')
        pygame.mixer.music.play()
        self.after(1000, self.destroy)

    def show_login_screen(self):
        self.geometry("398x648")
        self.resizable(False, False)  # Keep maximize button disabled on the login screen
        self.clear_frames()
        LoginScreen(self, self.login_success_callback)

    def login_success_callback(self, username, role):
        print(f"Logged in as {username} with role {role}")
        self.current_user = username
        self.current_user_role = role

        # Remove `overrideredirect` flag before moving to the next screen
        self.overrideredirect(False)

        # Show the dashboard screen after successful login
        self.show_dashboard_screen()

    def show_dashboard_screen(self):
        self.geometry("1000x700")  # Resize window for the dashboard
        self.resizable(True, True)  # Enable maximize button after login
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        DashboardScreen(self)

    def show_manage_screen(self):
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        ManageInventoryScreen(self, backend, self.current_user_role)

    def show_profile_screen(self):
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        ProfileScreen(self, self.current_user, self.current_user_role)

    def show_settings_screen(self):
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        SettingsScreen(self, self.current_user_role, backend)

    def show_manage_staff_screen(self):
        self.clear_frames(exclude_nav=True)
        self.create_or_update_navigation_pane()
        ManageStaffScreen(self, backend, self.current_user_role)

    def refresh_styles(self):
        """Refresh styles for all components after theme change."""
        if hasattr(self, 'nav_frame') and isinstance(self.nav_frame, CreateNavigationPane):
            self.nav_frame.refresh_styles()

    def show_terminate_screen(self):
        if self.current_user_role == 'Supervisor':
            self.clear_frames(exclude_nav=True)
            self.create_or_update_navigation_pane()
            TerminateUserScreen(self, backend)

    def show_generate_report_screen(self):
        # Launch the GenerateReportScreen module
        report_screen = GenerateReportScreen()
        report_screen.mainloop()  # Start the main loop for the report screen
        print("Reports screen launched successfully.")

    def clear_frames(self, exclude_nav=False):
        # Clear all frames except navigation if specified
        for widget in self.winfo_children():
            if exclude_nav and self.nav_frame and widget == self.nav_frame:
                continue
            if str(widget) in self.tk.call('winfo', 'children', self):
                try:
                    widget.destroy()
                except Exception as e:
                    print(f"Error destroying widget: {e}")

        if not exclude_nav and self.nav_frame:
            try:
                self.nav_frame.destroy()
                self.nav_frame = None
            except Exception as e:
                print(f"Error destroying nav_frame: {e}")

    def create_or_update_navigation_pane(self):
        # Destroy the existing nav_frame before creating a new one
        if self.nav_frame:
            try:
                self.nav_frame.destroy()
            except Exception as e:
                print(f"Error destroying nav_frame: {e}")

        # Prepare parameters based on user role
        if self.current_user_role == "Supervisor":
            show_manage_staff_screen = self.show_manage_staff_screen
            show_generate_report_screen = self.show_generate_report_screen
        else:
            show_manage_staff_screen = None
            show_generate_report_screen = None

        # Instantiate the navigation pane with the correct parameters
        self.nav_frame = CreateNavigationPane(
            self,
            self.show_dashboard_screen,
            self.show_manage_screen,
            self.show_profile_screen,
            self.show_settings_screen,
            show_manage_staff_screen=show_manage_staff_screen,
            show_generate_report_screen=show_generate_report_screen
        )


    def toggle_fullscreen(self):
        # Toggle between fullscreen and windowed mode
        if self.is_full_screen:
            self.attributes("-fullscreen", False)
            self.is_full_screen = False
        else:
            self.attributes("-fullscreen", True)
            self.is_full_screen = True


if __name__ == "__main__":
    app = InventoryApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Set up proper window close handling
    app.mainloop()