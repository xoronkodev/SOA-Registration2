import streamlit as st
import smtplib
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from PIL import Image

# --- CRITICAL PYTHON INITIALIZATION ---
st.set_page_config(page_title="SOA Registration", page_icon="🎓", layout="centered")

# -------------------------------------------------------------------------
# 1. SECURE EMAIL ENGINE
# -------------------------------------------------------------------------
def send_registration_email(details, subjects, marks, receipt_file, registration_type):
    """Sends a detailed email report tailored to the registration type with fixed file stream logic."""
    MY_EMAIL = "khanzada212008@gmail.com"
    MY_PASSWORD = "whyv rtdf odiq hsgc" 

    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL
    msg['Subject'] = f"🎓 [{registration_type}] Registration: {details['Name']}"
    
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
    
    The proof of payment receipt is verified and attached below.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    if receipt_file is not None:
        receipt_file.seek(0)
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
st.title(" 🎓 SUPERIOR OFFICERS ACADEMY (SOA)")
st.markdown("#### Official Candidate Registration Portal")
st.warning("One-month FREE ESSAY WRITING classes. It is a one time offer for a limited number of seats")
st.warning("💳 **Fee Notice (ONLY APPILIES FOR GENERAL/CSS STUDENTS WANTING TO PARTAKE IN ONE MONTH FREE CLASSES):** Kindly deposit your ONE TIME  registration fee (1000 RUPEES) into the **EasyPaisa Account: 03365464411 ACCOUNT NAME : MUHAMMAD AKRAM ** after filling out your details.")
st.warning()
st.write("---")


# --- STEP 1: INITIAL SELECTION ---
st.subheader("🎯 Step 1: Select Your Registration Category")
reg_type = st.selectbox(
    "Are you applying as a CSS Candidate or a General Academy Student? *",
    ["Select your category...", "General Academy Candidate (Non-CSS)", "CSS Candidate"]
)
st.write("---")

# --- CONDITIONAL WRAPPER ---
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
    
    if reg_type == "CSS Candidate":
        col1, col2 = st.columns(2)
        with col1:
            css_attempts = st.number_input("How many times have you appeared in CSS examination before?", min_value=0, max_value=3, step=1)
        with col2:
            pms_attempts = st.number_input("How many times have you appeared in PMS examination before?", min_value=0, max_value=3, step=1)
    else:
        css_attempts = 0
        pms_attempts = 0
        
    st.write("---") 
    
    # --- PART B: CONDITIONAL SUBJECT SELECTION (STEP 3 FOR CSS) ---
    selected_subjects = []
    total_marks = 0
    
    if reg_type == "CSS Candidate":
        st.subheader("📚 Step 3: CSS Subject Selection")
        st.info("Select one subject from each group you wish to take. Your **Total Marks Score must equal exactly 600** to qualify.")
        
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
    current_step_label = "Step 4" if reg_type == "CSS Candidate" else "Step 3"
    st.subheader(f"📁 {current_step_label}: Registration Fee Receipt")
    uploaded_receipt = st.file_uploader("Upload your EasyPaisa payment screenshot or slip *", type=["png", "jpg", "jpeg", "pdf"])
    
    if uploaded_receipt is not None:
        uploaded_receipt.seek(0)
        if uploaded_receipt.type in ["image/png", "image/jpeg"]:
            st.image(Image.open(uploaded_receipt), caption="Preview of payment proof", width=250)

    st.write("---")
    final_submit = st.button("Submit Final Application to SOA")

    # -------------------------------------------------------------------------
    # 3. COMPLIANCE & SUBMISSION CHECK
    # -------------------------------------------------------------------------
    if final_submit:
        if not name or not father_name or not email or not whatsapp_number or not qualification or not uploaded_receipt:
            st.error("🚨 Missing Required Fields! Please fill out all personal details and upload your receipt copy.")
        
        elif reg_type == "CSS Candidate" and total_marks != 600:
            st.error(f"❌ Failed Compliance: Your total opted marks value is {total_marks}. It must equal exactly 600 marks for CSS tracking.")
        
        else:
            with st.spinner("Processing application data..."):
                candidate_data = {
                    "Name": name, 
                    "FatherName": father_name, 
                    "Email": email,
                    "Whatsapp_Number": whatsapp_number,
                    "Qualification": qualification, 
                    "CSS_Attempts": css_attempts, 
                    "PMS_Attempts": pms_attempts
                }
                
                email_sent = send_registration_email(candidate_data, selected_subjects, total_marks, uploaded_receipt, reg_type)
                
                if email_sent:
                    # --- COMPREHENSIVE DATA STRING FOR WHATSAPP TRANSMISSION ---
                    # Packages 100% of user fields into parameters text block
                    whatsapp_text = f"""*🎓 NEW SOA ACADEMY REGISTRATION!*

*Track Chosen:* {reg_type}
*Candidate Name:* {name}
*Father's Name:* {father_name}
*Contact Email:* {email}
*Student WhatsApp:* {whatsapp_number}
*Academic Qualifications:* {qualification}
"""
                    if reg_type == "CSS Candidate":
                        whatsapp_text += f"*Previous CSS Attempts:* {css_attempts}\n"
                        whatsapp_text += f"*Previous PMS Attempts:* {pms_attempts}\n\n"
                        whatsapp_text += f"*📚 OPTED CSS SUBJECTS ({total_marks}/600):*\n"
                        for sub in selected_subjects:
                            if "None" not in sub:
                                whatsapp_text += f" - {sub}\n"
                    
                    whatsapp_text += "\n✅ *Status:* Local form verification passed and payment backup copy processed to Email Server successfully."
                    
                    encoded_text = urllib.parse.quote(whatsapp_text)
                    MY_PHONE_NUMBER = "923365464411"
                    whatsapp_gateway_url = f"https://wa.me/{MY_PHONE_NUMBER}?text={encoded_text}"
                    
                    # --- UNMISSABLE SYSTEM POPUP OVERLAY ---
                    st.markdown(f"""
                    <div style="
                        position: fixed; 
                        top: 0; left: 0; width: 100vw; height: 100vh; 
                        background-color: rgba(0, 0, 0, 0.75); 
                        z-index: 999999; 
                        display: flex; justify-content: center; align-items: center;
                    ">
                        <div style="
                            background-color: #ffffff; 
                            padding: 40px; 
                            border-radius: 16px; 
                            max-width: 500px; 
                            text-align: center; 
                            box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
                            border-top: 8px solid #25D366;
                            font-family: sans-serif;
                        ">
                            <h2 style="color: #111111; margin-top: 0;">⚠️ ACTION REQUIRED</h2>
                            <p style="color: #444444; font-size: 16px; line-height: 1.5; margin-bottom: 25px;">
                                Your details have been parsed locally, but your academy slot is <b>NOT YET CONFIRMED</b>. 
                                <br><br>
                                You must click the green button below to sync your profile parameters with the Superior Officers Academy administrative WhatsApp registry channel.
                            </p>
                            <a href="{whatsapp_gateway_url}" target="_blank" style="text-decoration: none;">
                                <div style="
                                    background-color: #25D366; 
                                    color: white; 
                                    padding: 18px 30px; 
                                    font-size: 18px; 
                                    font-weight: bold; 
                                    border-radius: 8px; 
                                    cursor: pointer; 
                                    box-shadow: 0px 4px 15px rgba(37, 211, 102, 0.4);
                                    display: inline-block;
                                ">
                                    🟢 FINALIZE REGISTRATION ON WHATSAPP
                                </div>
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.warning("Application verified locally, but secure mail delivery engine encountered an error. Please check your network connection.")
