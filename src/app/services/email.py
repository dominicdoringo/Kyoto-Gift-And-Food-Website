# src/app/services/email.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException

from app.core.config import settings

def send_verification_email(to_email: str, username: str, verification_code: str):
    """
    Sends a verification email to the specified user.
    """
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    smtp_username = settings.SMTP_USERNAME
    smtp_password = settings.SMTP_PASSWORD
    email_from = settings.EMAIL_FROM
    email_from_name = settings.EMAIL_FROM_NAME

    subject = "Verify Your Email"
    verification_link = f"http://localhost:8000/users/verify-email/{verification_code}"
    body = f"""
    Hi {username},

    Thank you for registering. Please verify your email by clicking on the link below:

    {verification_link}

    If you did not register on our platform, please ignore this email.

    Best regards,
    {email_from_name}
    """

    # Create the email message
    message = MIMEMultipart()
    message["From"] = f"{email_from_name} <{email_from}>"
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            server.sendmail(email_from, to_email, message.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
