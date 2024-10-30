
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import pandas as pd
from gmail_outlook import checkmail
from db import Database
from login_signup import login

db =  Database()

def gmail():
    st.header("Welcome to the Home Page")
    st.header("On Gmail")
    user_email = login.login().send_email()
    sender_email = str(db.send_user_email(user_email))
    password = "dimy cuho nckx dhiq"

    subject = st.text_input("Enter Subject",key="gmail_sub")
    message_text = st.text_area("Enter Message",key="gmail_msg")
    st.info("CSV file should have columns as: contact_email,Phone_number,Name")
    uploaded_file = st.file_uploader("Choose a CSV file that contains emails", type="csv",key="gmail_csv")

    recipients = []

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if 'contact_email' in df.columns:
            csv_recipients = df['contact_email'].tolist()
            csv_recipients_number = df['Phone_number'].tolist()
            csv_recipients_name = df['Name'].tolist()
            recipients.extend(csv_recipients)
        else:
            st.error("No 'contact_email' column found in the uploaded CSV file")
        
        if st.button("Save CSV mail"):
            for i in range(len(csv_recipients)):
                db.add_contact(str(sender_email),csv_recipients[i],
                               csv_recipients_name[i],csv_recipients_number[i])
 
    
    def display_contacts(user_email):
        contacts = db.get_contacts_by_email(user_email)

        # Display the user email
        if contacts:
            st.write(f"Contacts for: {user_email}")
            st.write("Contact List")

            # Create a table to show contacts with delete and update options
            for contact in contacts:
                contact_id, user_email, contact_email, name, phone_number = contact
                col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 2, 2, 1])

                # Display contact details in each row
                col1.write(contact_id)
                col2.write(contact_email)
                col3.write(name)
                col4.write(phone_number)

                # Delete and Update buttons for each contact
                if col5.button("Delete", key=f"delete_{contact_id}"):
                    db.delete_contact(user_email, contact_email)
                    st.success(f"Deleted contact: {contact_email}")
                    st.session_state.show_gmail_page = True
                     # Refresh the app to update the contact list

                if col6.button("Update", key=f"update_{contact_id}"):
                    new_name = st.text_input("New Name", value=name, key=f"name_{contact_id}")
                    new_phone = st.text_input("New Phone", value=phone_number, key=f"phone_{contact_id}")
                    if st.button("Save Changes", key=f"save_{contact_id}"):
                        db.update_contact(user_email, contact_email, new_name, new_phone)
                        st.success(f"Updated contact: {contact_email}")
        
        else:
            st.success("No contacts found")                  # Refresh the app to update the contact list
  
    if st.button("SeeMy contacts"):
        display_contacts(sender_email)

    
    
    
    
    
    def send_email(sender, password, recipient, subject, message):
        if checkmail.verfy_mail(recipient):
            try:
                mime_message = MIMEMultipart()
                mime_message['From'] = sender
                mime_message['To'] = recipient
                mime_message['Subject'] = subject

                mime_message.attach(MIMEText(message, 'plain'))  # Set to 'html' for tracking image

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender, password)
                    server.send_message(mime_message)
     
                st.success(f"Email sent successfully to {recipient}")
                return 1
            except Exception as e:
                st.success(f"An error occurred while sending to {recipient}: {e}")
        else:
            st.success("Email is wrong")
            return 0 
        
    send_count = 0
    if st.button("Send", key="Sending"):
        for recipient in recipients:
            send_count += send_email(sender_email, password, recipient, subject, message_text)
        failed_count = len(recipients) - send_count
        st.title("Gmail statistics")
        st.header("Total mail send") 
        st.header(send_count)
        st.header("Total mail failed")
        st.header(failed_count)