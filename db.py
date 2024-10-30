
import sqlite3
import bcrypt
import re

class Database:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name,check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_users_table()
        self.create_contacts_table()

    def create_users_table(self):
        """Create the users table if it doesn't exist."""
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def user_exists(self, email ,username):
        """Check if the user exists based on email or username."""
        self.c.execute("SELECT * FROM users WHERE email = ? OR username = ?", (email, username))
        return self.c.fetchone() is not None


    def register_user(self, email, username, password):
        """Register a new user after validation."""
        # Return the error message

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self.c.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return "Email or username already exists."  # This means the email or username already exists

    def verify_login(self, email_or_username, password):
        """Verify the user's login credentials."""
        self.c.execute("SELECT password FROM users WHERE email = ? OR username = ?", (email_or_username, email_or_username))
        result = self.c.fetchone()

        if result:  # If a user is found
            stored_password = result[0]
            return bcrypt.checkpw(password.encode('utf-8'), stored_password)

        return False  # User not found
    
    def send_user_email(self,user):
        self.c.execute("SELECT email FROM users WHERE username=? OR email=?",(user,user))
        result = self.c.fetchall()
        if result:
            user_email = result[0]
            return user_email
        else:
            return False
    def create_contacts_table(self):
        """Create the contacts table if it doesn't exist."""
        self.c.execute(""" 
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                contact_email TEXT NOT NULL,
                name TEXT,
                phone_number TEXT,
                FOREIGN KEY (email) REFERENCES users(email),
                UNIQUE(email, contact_email, name, phone_number)  -- Ensure unique combinations
            )
        """)
        self.conn.commit()

    def add_contact(self, user_email, contact_email, name, phone_number):
        """Add a new contact associated with the user."""
        try:
            self.c.execute("INSERT INTO contacts (email, contact_email, name, phone_number) VALUES (?, ?, ?, ?)", 
                        (user_email, contact_email, name, phone_number))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return "Contact already exists."
        
    def get_contacts_by_email(self, user_email):
        """Get all contacts for a specific user and contact email."""
        self.c.execute("SELECT * FROM contacts WHERE email = ?", (user_email))
        return self.c.fetchall()
    
    def update_contact(self, user_email, contact_email, name, phone_number):
        """Update a contact's details for the specified user and contact email."""
        self.c.execute("UPDATE contacts SET name = ?, phone_number = ? WHERE user_email = ? AND contact_email = ?", 
                    (name, phone_number, user_email, contact_email))
        self.conn.commit()

    def delete_contact(self, user_email, contact_email, name=None):
        """Delete a contact by email and optional name for the specified user."""
        if name:
            self.c.execute("DELETE FROM contacts WHERE user_email = ? AND contact_email = ? AND name = ?", 
                        (user_email, contact_email, name))
        else:
            self.c.execute("DELETE FROM contacts WHERE user_email = ? AND contact_email = ?", 
                        (user_email, contact_email))
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
