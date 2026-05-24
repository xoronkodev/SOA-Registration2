import streamlit as st
import smtplib
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from PIL import Image

# -------------------------------------------------------------------------
# 1. SECURE EMAIL ENGINE
# -------------------------------------------------------------------------
def send_registration_email(details, subjects, marks, receipt_file, registration_type):
    """Sends a detailed email report tailored to the registration type."""
    MY_EMAIL = "khanzada212008@gmail.com"
    MY_PASSWORD = "whyv rtdf odiq hsgc" 

    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL
    msg['Subject'] = f"🎓 [{registration_type}] Registration: {details['Name']}"
    
    # Format subjects if CSS user, otherwise keep it simple
    if registration_type == "CSS Candidate" and subjects:
        clean_subjects = [s for s in subjects if "None" not in s]
        subject_string = "\n".join([f" - {s}" for s in clean_subjects])
        academic_section = f"""--- ACADEMIC PATHWAY (CSS) ---
    Opted Subjects (Total Marks: {marks}):
{subject_string}"""
    else:
        academic_section = "--- ACADEMIC PATHWAY ---\n General Academy Course Registration (No CSS Subjects Required)"

    body = f"""
    A new candidate has successfully registered for Superior Officers Academy.

    Registration Category: {registration_type}

    --- CANDIDATE DETAILS ---
    Name: {details['Name']}
    Father's Name: {details['FatherName']}
    WhatsApp Number: {details['Whatsapp_Number']}
    Email Address: {details['Email']}
    Academic Qualification: {details['Qualification']}
    Previous CSS Attempts: {details['CSS_Attempts']}
    Previous PMS Attempts: {details['PMS_Attempts']}
    Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    {academic_section}
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
# 2. USER INTERFACE & APP LAYOUT
# -------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="SOA Registration", page_icon="🎓", layout="centered")
    
    st.title("🏛️ SUPERIOR OFFICERS ACADEMY (SOA)")
    st.markdown("#### Official Candidate Registration Portal")
    
    st.warning("💳 **Fee Notice:** Kindly deposit your registration fee into the **EasyPaisa Account: 03365464411** before filling out this form.")
    st.write("---")
    
    # --- STEP 1: INITIAL SELECTION WITH CUSTOM INITIAL TEXT ---
    st.subheader("🎯 Step 1: Select Your Registration Category")
    reg_type = st.selectbox(
        "Are you applying as a CSS Candidate or a General Academy Student? *",
        ["Select your category...", "General Academy Candidate (Non-CSS)", "CSS Candidate"]
    )
    st.write("---")

    # --- CONDITIONAL WRAPPER: ONLY EXECUTE IF A VALID OPTION IS SELECTED ---
    if reg_type == "Select your category...":
        st.info("👋 Welcome to the SOA Portal! Please select your category in Step 1 above to open the official registration form fields.")
    
    else:
        # --- PART A: PERSONAL DETAILS (STEP 2) ---
        st.subheader("👤 Step 2: Necessary Personal Details")
        
        name = st.text_input("Enter your name *")
        father_name = st.text_input("Enter your father's name *")
        email = st.text_input("Enter your email address *")
        whatsapp_number = st.text_input("Please enter your WhatsApp number *")
        qualification = st.text_area("Kindly describe your Academic Qualification *")
        
        # Dynamic display of attempts based on user type selection above
        if reg_type == "CSS Candidate":
            col1, col2 = st.columns(2)
            with col1:
                css_attempts = st.number_input("How many times have you appeared in CSS examination before?", min_value=0, max_value=3, step=1)
            with col2:
                pms_attempts = st.number
