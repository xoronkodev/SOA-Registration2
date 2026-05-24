import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from PIL import Image
from twilio.rest import Client

# -------------------------------------------------------------------------
# 1. SECURE WHATSAPP ENGINE
# -------------------------------------------------------------------------
def send_whatsapp_notification(details, total_marks):
    """Sends a real-time summary notification directly to your phone via WhatsApp."""
    TWILIO_ACCOUNT_SID = "AC7c6c5c8121c5287dd861758f57ac72cd"
    TWILIO_AUTH_TOKEN = "77f1dd75cca3a1ac5dc86f8151dc40a1"
    
    FROM_WHATSAPP = "whatsapp:+14155238886"
    TO_WHATSAPP = "whatsapp:+923365464411" 
    
    whatsapp_body = f"""
*🎓 New SOA Registration!*

*Candidate:* {details['Name']}
*Father's Name:* {details['FatherName']}
*Email:* {details['Email']}
*Student WhatsApp:* {details['Whatsapp_Number']}
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
    WhatsApp Number: {details['Whatsapp_Number']}
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
        whatsapp_number = st.text_input("Please enter your WhatsApp number *")
        qualification = st.text_area("Kindly describe your Academic Qualification *")
        
        col1, col2 = st.columns(2)
        with col1:
            css_attempts = st.number_input("How many times have you appeared in CSS examination before?", min_value=0, max_value=3, step=1)
        with col2:
            pms_attempts = st.number_input("How many times have you appeared in PMS examination before?", min_value=0, max_value=3, step=1)
        
        save_details = st.form_submit_button("Save Personal Info")
            
    st.write("---") 
    
    # --- PART B: LIVE SUBJECT SELECTION (OUTSIDE FORM) ---
    st.subheader("📚 Step 2: Subject Selection")
    st.info("Select one subject from each group you wish to take. Your **Total Marks Score must equal exactly 600** to qualify.")
    
    selected_subjects = []
    total_marks = 0
    
    g1_choice = st.selectbox("Select subject from Group 1 (200 Marks)", ["None", "Accounting & Auditing", "Economics", "Computer Science", "Political Science", "International Relations"])
    if g1_choice != "None":
        selected_subjects.append(f"{g1_choice} (200m)")
        total_marks += 200
        
    g2_choice = st.selectbox("Select subject from Group 2 (200 Marks)", ["None", "Physics", "Chemistry", "Applied Mathematics", "Pure Mathematics", "Statistics", "Geology"])
    if g2_choice != "None":
        selected_subjects.append(f"{g2_choice} (200m)")
        total_marks += 200
        
    g3_choice = st.selectbox("Select subject from Group 3 (100 Marks)", ["None", "Business Administration", "Public Administration", "Governance & Public Policy", "Town Planning & Urban Management"])
    if g3_choice != "None":
        selected_subjects.append(f"{g3_choice} (100m)")
        total_marks += 100
        
    g4_choice = st.selectbox("Select subject from Group 4 (100 Marks)", ["None", "History of Pakistan & India", "Islamic History & Culture", "British History", "European History", "History of USA"])
    if g4_choice != "None":
        selected_subjects.append(f"{g4_choice} (100m)")
        total_marks += 100
        
    g5_choice = st.selectbox("Select subject from Group 5 (100 Marks)", ["None", "Gender Studies", "Environmental Science", "Agriculture & Forestry", "Botany", "Zoology", "English Literature", "Urdu Literature"])
    if g5_choice != "None":
        selected_subjects.append(f"{g5_choice} (100m)")
        total_marks += 100

    g6_choice = st.selectbox("Select subject from Group 6 (100 Marks)", ["None", "Law", "Constitutional Law", "International Law", "Muslim Law & Jurisprudence", "Mercantile Law", "Criminology", "Philosophy"])
    if g6_choice != "None":
        selected_subjects.append(f"{g6_choice} (100m)")
        total_marks += 100

    g7_choice = st.selectbox("Select subject from Group 7 (100 Marks)", ["None", "Journalism and Mass Communication", "Psychology", "Geography", "Anthropology", "Sociology", "Punjabi", "Sindhi", "Balochi", "Pashto", "Persian", "Arabic"])
    if g7_choice != "None":
        selected_subjects.append(f"{g7_choice} (100m)")
        total_marks += 100

    st.metric(label="Current Opted Subject Marks Counter", value=f"{total_marks} / 600 Marks")
    st.write("---")
    
    # --- PART C: FINAL SUBMISSION & UPLOAD ---
    st.subheader("📁 Step 3: Registration Fee Receipt")
    uploaded_receipt = st.file_uploader("Upload your EasyPaisa payment screenshot or slip *", type=["png", "jpg", "jpeg", "pdf"])
    
    if uploaded_receipt is not None and uploaded_receipt.type in ["image/png", "image/jpeg"]:
        st.image(Image.open(uploaded_receipt), caption="Preview of payment proof", width=250)

    st.write("---")
    final_submit = st.button("Submit Final Application to SOA")

    # -------------------------------------------------------------------------
    # 4. COMPLIANCE & SUBMISSION CHECK
    # -------------------------------------------------------------------------
    if final_submit:
        if not name or not father_name or not email or not whatsapp_number or not qualification or not uploaded_receipt:
            st.error("🚨 Missing Required Fields! Please fill out all personal details (including your WhatsApp number) and upload your receipt copy.")
        
        elif total_marks != 600:
            st.error(f"❌ Failed Compliance: Your total opted marks value is {total_marks}. It must equal exactly 600 marks.")
        
        else:
            with st.spinner("Processing application data and broadcasting notifications..."):
                candidate_data = {
                    "Name": name, 
                    "FatherName": father_name, 
                    "Email": email,
                    "Whatsapp_Number": whatsapp_number,
                    "Qualification": qualification, 
                    "CSS_Attempts": css_attempts, 
                    "PMS_Attempts": pms_attempts
                }
                
                email_sent = send_registration_email(candidate_data, selected_subjects, total_marks, uploaded_receipt)
                whatsapp_sent = send_whatsapp_notification(candidate_data, total_marks)
                
                if email_sent:
                    st.success(f"🎉 Registration Successful! Thank you {name}. Your application has been sent securely to Superior Officers Academy.")
                    st.balloons()
                else:
                    st.warning("Application verified locally, but secure mail delivery engine encountered an error. Please check your network connection.")

if __name__ == "__main__":
    main()
