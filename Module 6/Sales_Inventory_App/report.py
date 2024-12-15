import customtkinter as ctk
from tkinter import filedialog, StringVar
import random
import csv
import os


class GenerateReportScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sales Report Generator")
        self.geometry("1000x700")
        self.configure(bg="#ecf0f1")  # Match the light background color of the dashboard

        # Title Section
        title_label = ctk.CTkLabel(
            self,
            text="Sales Report Dashboard",
            font=("Verdana", 28, "bold"),
            text_color="#2c3e50"  # Match the text color of the dashboard
        )
        title_label.pack(pady=20)

        # Filter Section
        filter_frame = ctk.CTkFrame(self, fg_color="#ecf0f1", corner_radius=10)
        filter_frame.pack(pady=10, padx=20, fill="x")

        # Filter Criteria Title
        filter_title = ctk.CTkLabel(
            filter_frame,
            text="Filter Criteria",
            font=("Verdana", 18, "bold"),
            text_color="#34495e"
        )
        filter_title.grid(row=0, column=0, columnspan=2, pady=10)

        # Dropdown for Salesperson
        self.salesperson_filter = StringVar(value="All Salespersons")
        ctk.CTkLabel(filter_frame, text="Salesperson:", font=("Verdana", 14), text_color="#2c3e50").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.salesperson_dropdown = ctk.CTkOptionMenu(filter_frame, variable=self.salesperson_filter, values=self.get_salespeople(), font=("Verdana", 14))
        self.salesperson_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Dropdown for Item
        self.item_filter = StringVar(value="All Items")
        ctk.CTkLabel(filter_frame, text="Item:", font=("Verdana", 14), text_color="#2c3e50").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.item_dropdown = ctk.CTkOptionMenu(filter_frame, variable=self.item_filter, values=self.get_items(), font=("Verdana", 14))
        self.item_dropdown.grid(row=2, column=1, padx=10, pady=5)

        # Generate Report Button
        generate_button = ctk.CTkButton(filter_frame, text="Generate Report", command=self.generate_report, font=("Verdana", 14, "bold"), corner_radius=10, fg_color="#27ae60", text_color="white")
        generate_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Report Display Section
        report_frame = ctk.CTkFrame(self, fg_color="#ecf0f1", corner_radius=10)
        report_frame.pack(pady=20, padx=20, fill="both", expand=True)

        report_title = ctk.CTkLabel(
            report_frame,
            text="Generated Sales Report",
            font=("Verdana", 18, "bold"),
            text_color="#34495e"
        )
        report_title.pack(pady=10)

        self.report_output = ctk.CTkTextbox(report_frame, height=400, font=("Verdana", 14), wrap="none", fg_color="#ffffff", text_color="#2c3e50", border_color="#34495e", border_width=2)
        self.report_output.pack(fill="both", expand=True, padx=20, pady=10)

        # Download Button
        download_button = ctk.CTkButton(self, text="Download CSV Report", command=self.download_report, font=("Verdana", 14, "bold"), corner_radius=10, fg_color="#2980b9", text_color="white")
        download_button.pack(pady=20)

        # Placeholder for generated report file
        self.generated_report_file = None

    def get_salespeople(self):
        """Retrieve a list of salespeople from the database."""
        # Replace with your database connection
        salespeople = ["All Salespersons", "John Doe", "Jane Smith", "Alice Johnson"]
        return salespeople

    def get_items(self):
        """Retrieve a list of items from the database."""
        # Replace with your database connection
        items = ["All Items", "Item A", "Item B", "Item C"]
        return items

    def generate_report(self):
        """Generate a detailed sales report based on the selected filters."""
        salesperson = self.salesperson_filter.get()
        item = self.item_filter.get()

        # Placeholder for database queries
        report_data = [
            {"Sale ID": 1, "Salesperson": "John Doe", "Item": "Item A", "Quantity": 3, "Total": 300},
            {"Sale ID": 2, "Salesperson": "Jane Smith", "Item": "Item B", "Quantity": 2, "Total": 200},
        ]  # Replace with actual database query

        self.generated_report_file = "sales_report.csv"
        with open(self.generated_report_file, "w", newline="") as csvfile:
            fieldnames = ["Sale ID", "Salesperson", "Item", "Quantity", "Total"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in report_data:
                writer.writerow(row)

        # Display data in the report output box
        self.report_output.delete("1.0", "end")
        self.report_output.insert("1.0", "Sales Report:\n\n")
        for row in report_data:
            self.report_output.insert("end", f"Sale ID: {row['Sale ID']}, Salesperson: {row['Salesperson']}, Item: {row['Item']}, "
                                              f"Quantity: {row['Quantity']}, Total: {row['Total']}\n")

    def download_report(self):
        """Download the generated CSV report to a selected folder."""
        if self.generated_report_file:
            save_path = filedialog.askdirectory(title="Select Folder to Save Report")
            if save_path:
                destination_path = os.path.join(save_path, self.generated_report_file)
                os.rename(self.generated_report_file, destination_path)
                ctk.CTkMessagebox.show_info("Success", "Report downloaded successfully!")
        else:
            print("No report generated yet.")


if __name__ == "__main__":
    app = GenerateReportScreen()
    app.mainloop()
