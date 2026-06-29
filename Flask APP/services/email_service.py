import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

class MailNotifier:
    def __init__(self):
        self.__sender = os.getenv("SENDER_MAIL")
        self.__password = os.getenv("SENDER_APP_PASSWORD")

    def _send_mail(self, reciever:str, subject:str, body:str):
        try:
            message = EmailMessage()
            message["From"] = self.__sender
            message["To"] = reciever
            message["Subject"] = subject
            message.set_content(body)
            
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                try:
                    server.login(self.__sender, self.__password)
                    server.send_message(message)
                except smtplib.SMTPAuthenticationError:
                    raise RuntimeError("Unable to Login smtp.gmail.com")
        
        except Exception as e:
            raise RuntimeError(f"Unable to send Email.\nError = {e}")


class EmailService:
    _mailer = MailNotifier()

    @staticmethod
    def send_approve_mail(email:str, request_id:int):
        subject = "Your leave has been Approved"
        approval_message = f"""
Dear Employee,

Your leave request has been approved.

Request ID : {request_id}

You may log in to the Leave Management System to view the complete details of your request.

Thank you.

Regards,
HR Department
Leave Management System
"""
        EmailService._mailer._send_mail(reciever=email, subject=subject, body=approval_message)

    @staticmethod
    def send_reject_mail(email:str, request_id:int):
        subject = "Your leave has been Rejected"
        rejection_message = f"""
Dear Employee,

We regret to inform you that your leave request has been rejected.

Request ID : {request_id}

You may log in to the Leave Management System to review the details of your request.

If you require further clarification, please contact the HR Department.

Regards,
HR Department
Leave Management System
"""
        
        EmailService._mailer._send_mail(reciever=email, subject=subject, body=rejection_message)

