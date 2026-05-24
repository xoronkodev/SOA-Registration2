import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from PIL import Image
from twilio.rest import Client  # Fixed: Capitalized Client to ensure clean launch

# -------------------------------------------------------------------------
# 1. SECURE WHATSAPP ENGINE
# -------------------------------------------------------------------------
def send_whatsapp_notification(details, total_marks):
    """Sends a real-time summary notification directly to your phone via WhatsApp."""
    # ⚠️ PLACE YOUR ACTUAL TWILIO CODES INSIDE THESE QUOTES:
    TWILIO_ACCOUNT_SID = "YOUR_REAL_ACCOUNT_SID"
    TWILIO_AUTH_TOKEN = "YOUR_REAL_AUTH_TOKEN"
    
    # Twilio Sandbox configurations
    FROM_WHATSAPP = "whatsapp:+14155238886"
    TO_WHATSAPP = "whatsapp:+923365464411" 
    
    whatsapp_body = f"""
*🎓 New SOA Registration!*

*Candidate:* {details['Name']}
*Father's Name:* {details['FatherName']}
*Email:* {details['Email']}
*Total Marks Opted:* {total_marks}/600

Check your inbox (khanzada212008@gmail.com) to view the complete subject selections and verify their attached payment receipt document.
"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=whatsapp_body,
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP
        )
        return True
    except Exception as e:
        print(f"WhatsApp Error: {e}")
        return False

# -------------------------------------------------------------------------
# 2. SECURE EMAIL ENGINE
# -------------------------------------------------------------------------
def send_registration_email(details, subjects, marks, receipt_file):
    """Sends an isolated, detailed email report for a single applicant."""
    MY_EMAIL = "khanzada212008@gmail.com"
    # Your verified internal Google app execution token
    MY_PASSWORD = "whyv rtdf odiq hsgc" 

    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL
    msg['Subject'] = f"🎓 SOA Registration: {details['Name']} ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    
    clean_subjects = [s for s in subjects if "None" not in s]
    subject_string = "\n".join([f" - {s}" for s in clean_subjects])
    
    body = f"""
    A new candidate has successfully registered for Superior Officers Academy.

    --- CANDIDATE DETAILS ---
    Name: {details['Name']}
    Father's Name: {details['FatherName']}
    Email Address: {details['Email']}
    Academic Qualification: {details['Qualification']}
    Previous CSS Attempts: {details['CSS_Attempts']}
    Previous PMS Attempts: {details['PMS_Attempts']}
    Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    --- ACADEMIC PATHWAY ---
    Opted Subjects (Total Marks: {marks}):
{subject_string}
    -------------------------
    
    The proof of payment receipt is attached below.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    if receipt_file is not None:
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload(receipt_file.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', f'attachment; filename={receipt_file.name}')
        msg.attach(payload)
        receipt_file.seek(0)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(MY_EMAIL, MY_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

# -------------------------------------------------------------------------
# 3. USER INTERFACE & APP LAYOUT
# -------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="SOA Registration", page_icon="🎓", layout="centered")
    
    st.title("🏛️ SUPERIOR OFFICERS ACADEMY (SOA)")
    st.markdown("#### Official Candidate Registration Portal")
    
    st.warning("💳 **Fee Notice:** Kindly deposit your registration fee into the **EasyPaisa Account: 03365464411** before filling out this form.")
    st.write("---")
    
    # --- PART A: PERSONAL DETAILS FORM ---
    with st.form(key="personal_details_form"):
        st.subheader("👤 Step 1: Necessary Personal Details")
        
        name = st.text_input("Enter your name *")
        father_name = st.text_input("Enter your father's name *")
        email = st.text_input("Enter your email address *")
        qualification = st.text_area("Kindly describe your Academic Qualification *")
        
        col1, col2 = st.columns(2)
        with col1:
            css_attempts = st.number_input("How many times have you appeared in CSS examination before?", min_value=0, max_value=3, step=1)
        with col2:
            pms_attempts = st.number_input("How many times have you appeared in PMS examination before?", min_value=0, max_value=3, step=1)
        
        save_details = st.form_submit_button("Save Personal Info")
            
    st.write
