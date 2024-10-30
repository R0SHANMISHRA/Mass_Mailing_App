import streamlit as st
from db import Database


db = Database()  # Initialize the database connection
global email_or_username
def login():
    st.title("Welcome, to Mass Mailing Application")
    st.header("Login to your account")
   
    email_or_username = st.text_input("Email/Username", placeholder="Enter your email or username",key="username_or_email")
    password = st.text_input("Password", type="password", placeholder="Enter your password",key="password")
    def send_email():
                if "email_or_username" in st.session_state:
                    return db.send_user_email(st.session_state[email_or_username])
                else:
                    st.warning("Please log in first.")
                    return None 
    

    if st.button("Login",help="Please do double click"):
        if db.verify_login(email_or_username, str(password)):
            # if st.button("Send using Gmail",key="Gmail"):
            st.session_state["email_or_username"] = email_or_username       
            st.session_state.show_gmail_page = True
            st.session_state.show_outlook_page = True
            st.success("You have logged In")
            
            
            return True
        else:
            st.error("Wrong email/username or password")
            return False
        
    if st.button("New User? Create a account",key="signup button",help="Double click"):
        st.session_state.show_login = False
        st.session_state.show_signup = True


        
    

  
