# Zero Trust Multi-Factor Authentication System (ZT-MFA)

A secure authentication system based on the Zero Trust Architecture (ZTA) model. This project integrates Multi-Factor Authentication (MFA) using password, One-Time Password (OTP), and biometric face recognition with anti-spoofing detection to ensure robust user verification.

## 🔐 Features

- ✅ **Zero Trust Architecture (ZTA)** principles
- 🔑 **Password Authentication** with hashed storage
- 📧 **Email-based OTP Verification**
- 👁️ **Face Recognition** with real-time anti-spoofing

## 📁 Project Structure

```
.
├── main.py                  # Entry point
├── face_recognition/        # Face detection and recognition modules
├── anti_spoofing/           # YOLO model and spoof detection
├── otp_service/             # OTP generation and email sending
├── database/                # User info and login data (SQLite)
├── utils/                   # Helper functions
├── user.db                  # Local user database
└── README.md                # This file
```

## 🚀 How to Run

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/zero-trust-mfa.git
   cd zero-trust-mfa
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure email (for OTP)**
   - Set up a Gmail account and allow less secure app access or use an app-specific password.

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 📷 Face Recognition & Anti-Spoofing

- Users are authenticated by matching their real-time face from webcam with the stored profile image.
- Anti-spoofing ensures the face is live and not a photo, video, or mask using a YOLO-based model.

## 🛡️ Security Principles

- **Verify Explicitly:** MFA with email OTP and facial biometrics
- **Least Privilege Access:** Only valid users access system resources
- **Assume Breach:** All access is re-verified; spoof attempts are blocked
