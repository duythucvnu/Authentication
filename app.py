import streamlit as st
import sqlite3
import bcrypt
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image
import biometric
import io
import os  # Import the os module

# 🔑 Email SMTP Configuration
EMAIL_SENDER = "trungkien08033@gmail.com"
EMAIL_PASSWORD = "zrxgxxmjgtlixgfp"

# 🔑 Database Connection
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 email TEXT UNIQUE,
                 password TEXT,
                 profile_picture TEXT)''')  # Change BLOB to TEXT, storing the file path
    conn.commit()
    conn.close()

# 🔑 Hash Password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# 🔓 Verify Password
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# 🔄 Reset Password
def reset_password(email, new_password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    hashed_pw = hash_password(new_password)
    c.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_pw, email))
    conn.commit()
    conn.close()

# 📌 Register User
def register_user(username, email, password, profile_picture_path):  # Accept file path
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        hashed_pw = hash_password(password)
        c.execute("INSERT INTO users (username, email, password, profile_picture) VALUES (?, ?, ?, ?)", (username, email, hashed_pw, profile_picture_path))  # Store file path
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# 🚪 Login User
def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT email, password, profile_picture FROM users WHERE username = ?", (username,))  # Retrieve file path
    user = c.fetchone()
    conn.close()

    if user:
        email, stored_hashed_password, profile_picture_path = user
        if check_password(password, stored_hashed_password):
            return email, profile_picture_path  # Return file path as well
    return None, None

# 📩 Send OTP via Email
def send_otp(email):
    otp = str(random.randint(100000, 999999))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = email
        msg["Subject"] = "Login OTP Code"

        body = f"Your OTP code is: {otp}"
        msg.attach(MIMEText(body, "plain", "utf-8"))

        server.sendmail(EMAIL_SENDER, email, msg.as_string())
        server.quit()

        # Store OTP in session
        st.session_state["otp"] = otp
        st.session_state["login_email"] = email

        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False


# 🔑 Create Profile Picture Directory
PROFILE_PICTURE_DIR = "images/data"
if not os.path.exists(PROFILE_PICTURE_DIR):
    os.makedirs(PROFILE_PICTURE_DIR)

if "reset" not in st.session_state:
    st.session_state.reset = 0

# 📌 Navigation Menu
menu = ["Login", "Register", "Forgot Password"]
choice = st.sidebar.selectbox("Select Option", menu)

st.markdown("<div class='login-box'>", unsafe_allow_html=True)

if "biometric" in st.session_state and st.session_state["biometric"]:
        if "profile_picture" in st.session_state and st.session_state["profile_picture"]:
            profile_picture_path = st.session_state["profile_picture"]
            st.session_state["biometric"] = False
            biometric.authentication(profile_picture_path)

# ✅ **Welcome Screen if Logged In**
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.markdown(f"<h2>🎉 Welcome, {st.session_state['username']}!</h2>", unsafe_allow_html=True)

    # Display profile picture if available
    if "profile_picture" in st.session_state and st.session_state["profile_picture"]:
        profile_picture_path = st.session_state["profile_picture"]
        try:
            image = Image.open(profile_picture_path)
            st.image(image, caption="Profile Picture", width=100)  # Adjust width as needed
        except FileNotFoundError:
            st.error("Profile picture not found.")
        except Exception as e:
            st.error(f"Error displaying profile picture: {e}")
    else:
        st.write("No profile picture available.")

    st.write("You have successfully logged in. Have a great day! ☕😊")

    if st.button("🔓 Logout"):
        del st.session_state["logged_in"]
        del st.session_state["username"]
        del st.session_state["profile_picture"]  # Clear profile_picture from session too
        st.rerun()

# ✅ **Register Form**
elif choice == "Register":
    st.markdown("<h2>📌 <strong>Register Account</strong></h2>", unsafe_allow_html=True)
    new_user = st.text_input("Username")
    email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    profile_picture_file = st.file_uploader("Choose Profile Picture", type=["jpg", "jpeg", "png"])  # Image uploader

    if st.button("Register"):
        if new_user and email and new_password and profile_picture_file:  # Check if a file was uploaded
            try:
                # Save the uploaded file to the profile_pictures directory
                image = Image.open(profile_picture_file) #Open file
                filename = f"{new_user}_{profile_picture_file.name}"
                file_path = os.path.join(PROFILE_PICTURE_DIR, filename)

                image.save(file_path)

                if register_user(new_user, email, new_password, file_path):  # Pass file path to registration
                    st.success("🎉 Registration successful! Please log in.")
                else:
                    st.error("⚠️ Username or email already exists! Please try again.")

            except Exception as e:
                st.error(f"Error saving or processing image: {e}")
        else:
            st.warning("⚠️ Please fill in all fields and upload a profile picture.")


# ✅ **Login Form**
elif choice == "Login":
    st.markdown("<h2>🔓 <strong>Login</strong></h2>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        email, profile_picture_path = login_user(username, password)  # Get file path
        if email:
            if send_otp(email):
                st.success("✅ OTP has been sent! Please check your email.")
                st.session_state["pending_username"] = username
                st.session_state["pending_profile_picture"] = profile_picture_path  # Store file path for OTP page
        else:
            st.error("🚫 Incorrect username or password.")

    if "otp" in st.session_state:
        user_otp = st.text_input("Enter OTP", key="otp_login")

        if st.button("Verify OTP"):
            if user_otp == st.session_state["otp"]:
                email, profile_picture_path = login_user(username, password)
                st.session_state["biometric"] = True
                st.success(f"🎉 Login successful! Welcome, {st.session_state['pending_username']}.")

                st.session_state["logged_in"] = True
                st.session_state["username"] = st.session_state["pending_username"]
                st.session_state["profile_picture"] = st.session_state["pending_profile_picture"]  # Load file path

                del st.session_state["otp"]
                del st.session_state["login_email"]
                del st.session_state["pending_username"]
                del st.session_state["pending_profile_picture"]

                st.rerun()
            else:
                st.error("🚫 Incorrect OTP!")

# ✅ **Forgot Password**
elif choice == "Forgot Password":
    st.markdown("<h2>🔄 <strong>Forgot Password</strong></h2>", unsafe_allow_html=True)
    email = st.text_input("Enter your email")

    if st.button("Send OTP"):
        if send_otp(email):
            st.success("✅ OTP has been sent! Please check your email.")

    if "otp" in st.session_state:
        user_otp = st.text_input("Enter OTP", key="otp_input")
        new_password = st.text_input("Enter new password", type="password", key="new_password_reset")

        if st.button("Reset Password"):
            if user_otp == st.session_state["otp"]:
                if "login_email" in st.session_state and st.session_state["login_email"]:
                    reset_password(st.session_state["login_email"], new_password)
                    st.success("🔄 Password updated successfully! Please log in again.")
                    del st.session_state["otp"]
                    del st.session_state["login_email"]
                else:
                    st.error("🚫 Email not found for password reset!")
            else:
                st.error("🚫 Incorrect OTP!")

st.markdown("</div>", unsafe_allow_html=True)

init_db()