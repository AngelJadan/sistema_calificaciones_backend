from email.message import EmailMessage
from app_notas.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT
import smtplib


def send_mai(subject, to_email, message):
    """
    subject
    to_email,
    message
    """
    mail = EmailMessage()
    mail["From"] = EMAIL_HOST_USER
    mail["To"] = to_email
    mail["Subject"] = subject
    mail.set_content(message)
    with smtplib.SMTP("smtp.gmail.com", EMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        smtp.send_message(mail)
    return True
