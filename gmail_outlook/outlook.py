import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st
import pandas as pd
from gmail_outlook import checkmail


def outlook():
    st.header("On Outlook")
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    # smtp_user = "roshanmishra200407@gmail.com"
    smtp_user = "support@aptpath.in"
    # smtp_password = "ijifjcqpdutxktmo"
    smtp_password = "kjydtmsbmbqtnydk"
    # sender_email = "roshanmishra200407@gmail.com" 
    sender_email = "support@aptpath.in" 
    recipient_emails = []  # List of recipients
    subject = st.text_input("Enter Subject",key="Outlook_sub")
    message_text = st.text_area("Enter Message",key="Outlook_msg")
    uploaded_file = st.file_uploader("Choose a CSV file that contains emails", type="csv",key="outlook_csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if 'email' in df.columns:
            csv_recipients = df['email'].tolist()
            recipient_emails.extend(csv_recipients)
        else:
            st.error("No 'email' column found in the uploaded CSV file")


    def send_email(smtp_user,smtp_password,sender_email,recipient_email,subject,message_text):
        if checkmail.verfy_mail(recipient):
            try:
            
                mime_message = MIMEMultipart()
                mime_message['From'] = sender_email
                mime_message['To'] = recipient
                mime_message['Subject'] = subject
  
                mime_message.attach(MIMEText(message_text, 'plain')) 


                with smtplib.SMTP("smtp.office365.com",587) as server:
                    server.starttls()
                    server.login(smtp_user,smtp_password)
                    server.send_message(mime_message)
                st.success(f"Email sent successfully to {recipient}")
                return 1
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return 0
        else:
            st.error("Email is wrong")
            return 0 

    send_count = 0
    if st.button("Send",key="Outlook_Mail"):
        for recipient in recipient_emails: 
            send_count += send_email(
                    smtp_user,
                    smtp_password,
                    sender_email,
                    recipient,
                    subject,message_text)
        failed_count = len(recipient_emails) - send_count
        st.title("Outlook statistics")
        st.header("Total mail send") 
        st.header(send_count)
        st.header("Total mail failed")
        st.header(failed_count)



