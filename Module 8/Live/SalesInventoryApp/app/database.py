import sqlite3

# Function to create the users database
def create_database():
    """Creates the users database and the 'users' table if they do not exist."""
    try:
        conn = sqlite3.connect(r'db/Sales_Inventory.db')
        cursor = conn.cursor()
        # Create the users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating the database: {e}")
    finally:
        conn.close()

def initialize_database():
    conn = sqlite3.connect(r'db/Sales_Inventory.db')
    cursor = conn.cursor()
    # Create user_activity table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        );
    ''')
    # Create clock_times table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clock_times (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            clock_in DATETIME,
            clock_out DATETIME,
            FOREIGN KEY (username) REFERENCES users(username)
        );
    ''')
    conn.commit()
    conn.close()


# Function to fetch all users from the database
def fetch_users():
    """Fetches all usernames from the users table."""
    try:
        conn = sqlite3.connect(r'db/Sales_Inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        users = [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")
        users = []
    finally:
        conn.close()
    return users

# Function to remove a user from the database
def remove_user(username):
    """Removes a user from the users table based on the provided username."""
    try:
        conn = sqlite3.connect(r'db/Sales_Inventory.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error removing user '{username}': {e}")
    finally:
        conn.close()
