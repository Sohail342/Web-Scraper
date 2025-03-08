import random
import logging
from email.mime.text import MIMEText
from aiosmtplib import SMTP
from web_scraper.config import Config

logging.basicConfig(level=logging.DEBUG)

# Generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))


# Send an email with the OTP code
async def send_email_otp(email: str, otp_code: str):
    # Create the email message
    message = MIMEText(f"Your OTP code is: {otp_code}")
    message["From"] = Config.EMAIL_USERNAME
    message["To"] = email
    message["Subject"] = "OTP Verification Code"

    # Connect to the SMTP server and send the email
    async with SMTP(hostname=Config.EMAIL_HOST, port=Config.EMAIL_PORT, username=Config.EMAIL_USERNAME, password=Config.EMAIL_PASSWORD) as smtp:
        await smtp.send_message(message)
        logging.info(f"OTP email sent to {email}")