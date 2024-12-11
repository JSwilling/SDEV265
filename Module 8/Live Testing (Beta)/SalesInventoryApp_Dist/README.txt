The SalesInventoryApp is a comprehensive inventory management software designed to streamline inventory tracking, sales reporting, and user management. This application is built with Python and provides an intuitive graphical interface for users of all technical levels.

Features
Login System: Secure login with role-based access control.
Inventory Management: Add, edit, delete, and search inventory items.
Sales Reporting: Generate detailed sales reports for specified items.
User Management: Supervisors can manage staff, including adding and terminating users.
Settings: Customize themes, audio, and preferences.
Data Visualization: Interactive graphs for sales trends.
Requirements
Operating System: Windows 10 or later.
Python Version: Not required (this is a standalone .exe application).
RAM: At least 2GB (4GB recommended).
How to Install
Download:

Download the SalesInventoryApp_Dist.zip file from the provided link.
Extract:

Right-click the SalesInventoryApp_Dist.zip file and select Extract All.
Ensure all files are extracted into the same folder.
Run the Application:

Double-click on the main.exe file to start the application.
Follow the on-screen instructions to log in and manage your inventory.
File Structure
plaintext
Copy code
SalesInventoryApp/
├── main.exe                     # Main executable file
├── static/                      # Static assets
│   ├── images/                  # Image assets for the GUI
│   └── audio/                   # Audio files (e.g., logout and close sounds)
├── db/                          # Database folder
│   └── Sales_Inventory.db       # SQLite database for the application
├── README.md                    # Documentation file
Usage
Logging In:

Enter your username and password on the login screen.
Based on your role, you'll be redirected to the appropriate dashboard.
Managing Inventory:

Navigate to the Inventory tab to view, add, update, or delete items.
Generating Reports:

Go to the Reports tab and select an item ID to generate a detailed sales report.
User Management (Supervisors):

Access the Manage Staff section to add or remove users.
Settings:

Adjust the theme, audio, and other preferences in the Settings menu.
Known Issues
Ensure the database (Sales_Inventory.db) is in the db folder; otherwise, the app will fail to load data.
Some antivirus programs might flag .exe files. If this happens, mark the file as safe in your antivirus settings.
Troubleshooting
Problem: The app doesn't launch.

Solution: Verify that all files (especially db/Sales_Inventory.db and static/) are present in the same directory as main.exe.
Problem: Missing images or audio.

Solution: Ensure the static/ folder contains the correct subfolders (images/ and audio/).
Future Enhancements
Cloud-based database integration.
Cross-platform compatibility for macOS and Linux.
Real-time collaborative inventory management.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For support, contact the development team at support@salesinventoryapp.com.

