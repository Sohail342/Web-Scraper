import smtplib
import random
from email.mime.text import MIMEText
from web_scraper.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD

# Generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Send OTP via Email
def send_email_otp(email: str, otp_code: str):
    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp_code}. It is valid for 5 minutes."

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USERNAME
    msg["To"] = email

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")
