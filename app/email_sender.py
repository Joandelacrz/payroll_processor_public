import os 
import smtplib  # Para manejar el envío de correos
from email.message import EmailMessage  # Para estructurar el mensaje del email

def send_email(recipient, pdf_path):
    """
    Envía un correo con un archivo PDF adjunto.
    recipient: Email del destinatario.
    pdf_path: Ruta del archivo PDF a enviar.
    """

    # Obtiene las credenciales del remitente desde las variables de entorno
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')

    # Configura el servidor SMTP, usa Gmail por defecto
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))  # Puerto estándar para SMTP con TLS

    # Verifica que el correo y la contraseña del remitente estén configurados
    if not sender_email or not sender_password:
        print("Sender email credentials are not set. Email not sent.")
        return  # Sale de la función si faltan credenciales

    # Construye el mensaje del correo
    msg = EmailMessage()
    msg['Subject'] = 'Your Paystub'  
    msg['From'] = sender_email  
    msg['To'] = recipient  
    msg.set_content('Please find your attached paystub.') 

    # Intenta adjuntar el archivo PDF
    try:
        with open(pdf_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(pdf_path)  # Obtiene el nombre del archivo
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)
    except Exception as e:
        print(f"Error attaching PDF: {e}")
        return 

    # Intenta enviar el correo
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Habilita cifrado TLS
            server.login(sender_email, sender_password)  # Inicia sesión en SMTP
            server.send_message(msg)  # Envía el correo
            print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Error sending email to {recipient}: {e}")  # Captura errores en el envío
