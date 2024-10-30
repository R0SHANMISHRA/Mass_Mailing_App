import streamlit as st
from db import Database
from login_signup import login, signup
from gmail_outlook import gmail,outlook
import streamlit.components.v1 as com
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Initialize session state variables
if 'show_login' not in st.session_state:
    st.session_state.show_login = True
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False
if "show_gmail_page" not in st.session_state:
    st.session_state.show_gmail_page = False
if "show_outlook_page" not in st.session_state:
    st.session_state.show_outlook_page = False



if st.session_state.show_login:
    if login.login():
        st.session_state.show_login = False


if st.session_state.show_signup:
    st.session_state.show_login = False
    signup.signup()  



if st.session_state.show_gmail_page: 
    gmail.gmail()
    

if st.session_state.show_outlook_page:
   outlook.outlook() 


