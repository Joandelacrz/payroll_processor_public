import os
import smtplib
from email.message import EmailMessage

def send_email(recipient, pdf_path):
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))

    if not sender_email or not sender_password:
        print("Sender email credentials are not set. Email not sent.")
        return

    msg = EmailMessage()
    msg['Subject'] = 'Your Paystub'
    msg['From'] = sender_email
    msg['To'] = recipient
    msg.set_content('Please find your attached paystub.')

    try:
        with open(pdf_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(pdf_path)
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)
    except Exception as e:
        print(f"Error attaching PDF: {e}")
        return

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")

    def send_email(recipient, pdf_file):
        """
        Real function that sends email. We'll monkeypatch this in tests
        so we don't send real emails.
        """
        return {"email": recipient, "timestamp": "2025-02-12T14:00:00Z"}
