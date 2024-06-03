class SendMail(email=str, message=str):
    mail = EmailMessage()
        mail["From"] = EMAIL_HOST_USER
        mail["To"] = "angel.jadan12@gmail.com"  # documento.correo_cliente
        mail["Subject"] = "Error generado"
        mail.set_content(f"Error {sms} documento {documento}, tipo: {tipo}")

        with smtplib.SMTP("smtp.gmail.com", EMAIL_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            smtp.send_message(mail)
        return True