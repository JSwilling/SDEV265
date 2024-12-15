import customtkinter as ctk
from tkinter import filedialog, StringVar
import random
import csv
import os
import customtkinter
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
import sqlite3
import threading
import time
import pygame


class GenerateReportPopup(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Generate Sales Report")
        self.geometry("600x500")
        self.parent = parent

        self.transient(parent)  # Associate with the parent window
        self.grab_set()  # Block interaction with the parent window
        self.focus_force()  # Force focus on the popup

        # Disable resizing (optional)
        self.resizable(False, False)

        # Database connection
        self.db_path = r'db/Sales_Inventory.db'

        # UI Elements
        self.setup_ui()

    def setup_ui(self):
        # Filter Options
        self.filter_frame = customtkinter.CTkFrame(self)
        self.filter_frame.pack(pady=10, fill="x")

        # Agent ID Dropdown
        self.agent_id_var = tk.StringVar(value="All")
        self.agent_dropdown = ttk.Combobox(
            self.filter_frame, textvariable=self.agent_id_var, state="readonly"
        )
        self.agent_dropdown['values'] = self.get_agent_ids()
        self.agent_dropdown.grid(row=0, column=0, padx=10, pady=10)
        self.agent_dropdown_label = customtkinter.CTkLabel(
            self.filter_frame, text="Filter by Agent ID:"
        )
        self.agent_dropdown_label.grid(row=0, column=1, padx=10, pady=10)

        # Item ID Dropdown
        self.item_id_var = tk.StringVar(value="All")
        self.item_dropdown = ttk.Combobox(
            self.filter_frame, textvariable=self.item_id_var, state="readonly"
        )
        self.item_dropdown['values'] = self.get_item_ids()
        self.item_dropdown.grid(row=1, column=0, padx=10, pady=10)
        self.item_dropdown_label = customtkinter.CTkLabel(
            self.filter_frame, text="Filter by Item ID:"
        )
        self.item_dropdown_label.grid(row=1, column=1, padx=10, pady=10)

        # Generate Button
        self.generate_button = customtkinter.CTkButton(
            self, text="Generate Report", command=self.start_report_generation
        )
        self.generate_button.pack(pady=10)

        # Results Display Area
        self.results_frame = customtkinter.CTkFrame(self)
        self.results_frame.pack(pady=10, fill="both", expand=True)

        self.results_table = ttk.Treeview(self.results_frame, columns=("OrderID", "AgentID", "ItemID", "Quantity", "Date"), show="headings")
        for col in ("OrderID", "AgentID", "ItemID", "Quantity", "Date"):
            self.results_table.heading(col, text=col)
            self.results_table.column(col, anchor="center")
        self.results_table.pack(fill="both", expand=True)

        # Download Button
        action_frame = tk.Frame(self)
        action_frame.pack(pady=20)

        # Modify button size and style
        export_button = tk.Button(
            action_frame,
            text="Download CSV",
            command=self.download_csv,
            font=("Arial", 14),  # Adjust font size for larger buttons
            width=15,
            height=2,

        )
        export_button.grid(row=0, column=0, padx=15)

        close_button = tk.Button(
            action_frame,
            text="Close",
            command=self.on_close,
            font=("Arial", 14),  # Adjust font size for larger buttons
            width=15,  # Adjust width
            height=2,

        )
        close_button.grid(row=0, column=1, padx=15)

    def get_agent_ids(self):
        # Fetch unique agent IDs
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT agent_id FROM orders")
        agent_ids = [str(row[0]) for row in cursor.fetchall()]
        conn.close()
        return ["All"] + agent_ids

    def get_item_ids(self):
        # Fetch unique item IDs
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT item_id FROM orders")
        item_ids = [str(row[0]) for row in cursor.fetchall()]
        conn.close()
        return ["All"] + item_ids

    def start_report_generation(self):
        # Show loading screen
        self.show_loading_screen()

        # Run report generation in a separate thread
        threading.Thread(target=self.generate_report).start()

    def show_loading_screen(self):
        self.loading_frame = customtkinter.CTkFrame(self, fg_color="#c0392b", width=300, height=150)
        self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.loading_label = customtkinter.CTkLabel(
            self.loading_frame, text="Generating Report...", font=("Arial", 18, "bold"), text_color="white"
        )
        self.loading_label.pack(pady=20)

        self.loading_spinner = customtkinter.CTkProgressBar(self.loading_frame, orientation="horizontal")
        self.loading_spinner.pack(pady=10, padx=20)
        self.loading_spinner.start()

    def hide_loading_screen(self):
        self.loading_frame.destroy()

    def generate_report(self):
        time.sleep(2)  # Simulate processing delay

        # Clear previous results
        for item in self.results_table.get_children():
            self.results_table.delete(item)

        # Build query
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = "SELECT order_id, agent_id, item_id, quantity, order_date FROM orders WHERE 1=1"
        params = []

        if self.agent_id_var.get() != "All":
            query += " AND agent_id = ?"
            params.append(self.agent_id_var.get())

        if self.item_id_var.get() != "All":
            query += " AND item_id = ?"
            params.append(self.item_id_var.get())

        cursor.execute(query, params)
        orders = cursor.fetchall()
        conn.close()

        # Populate results table
        for order in orders:
            self.results_table.insert("", "end", values=order)

        # Save results for download
        self.generated_results = orders

        # Hide loading screen
        self.hide_loading_screen()

    def on_close(self):
        # Play logout sound before closing
        pygame.mixer.init()
        pygame.mixer.music.load(r'static/audio/logout.mp3')
        pygame.mixer.music.play()
        self.after(1000, self.destroy)

    def download_csv(self):
        if not hasattr(self, 'generated_results') or not self.generated_results:
            messagebox.showerror("Error", "No data to download. Generate a report first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["OrderID", "AgentID", "ItemID", "Quantity", "Date"])
                writer.writerows(self.generated_results)
            messagebox.showinfo("Success", f"Report saved to {file_path}")