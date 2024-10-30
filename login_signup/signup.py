import streamlit as st
from db import Database
import re
from login_signup import login

db = Database()  # Initialize the database connection

def is_valid_password(password):
    """Check if the password meets the requirements."""
    if (len(password) < 8 or
            not re.search(r"[A-Z]", password) or  # At least one uppercase letter
            not re.search(r"[a-z]", password) or  # At least one lowercase letter
            not re.search(r"[0-9]", password) or  # At least one number
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):  # At least one special character
        return False
    return True

def is_valid_email(email):
    """Check if the email is in a valid format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_username(username):
    """Check if the username meets length requirements."""
    return len(username) >= 3 

def signup():
    st.title("Welcome, to Mass Mailing Application")
    st.header("Create a account")
    
    email = st.text_input("Email", placeholder="Enter your email",key="Email")
    username = st.text_input("Username", placeholder="Enter your username",key="username")
    password = st.text_input("Password", type="password", placeholder="Enter your password",key="ppassword")

    if st.button("Sign Up"):
        if not email or not username or not password:
            st.error("Please fill in all fields.")
        elif not is_valid_email(email):
            st.error("Enter valid email")
        elif not is_valid_username(username):
            st.error("Minimum length should be of 3")
        elif not is_valid_password(password):
            st.error("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
        elif db.user_exists(email, username):
            st.error("Email or username already exists.")
        else:
            if db.register_user(email, username, password):
                st.success("You are registered")
                return True
            else:
                return False

    if st.button("Have account? Login",help="double click"):
       
        st.session_state.show_signin = False
        st.session_state.show_login = True
        login.login()

