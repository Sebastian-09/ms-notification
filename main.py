import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# funcion para enviar correos
def send_email(subject, recipient_email, body_html):
    email_sender = os.getenv('GoogleMail__EmailSender')
    email_password = os.getenv('GoogleMail__ApiKey')
    smtp_server = os.getenv('GoogleMail__Host')
    smtp_port = os.getenv('GoogleMail__Port')
    
    print(f'Email sender: (email_sender)')
    print(f'Email password: (email_password)')
    print(f'SMTP server: (smtp_server)')
    print(f'SMTP port: (smtp_port)')
    
    # crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = recipient_email 
    msg['Subject'] = subject
    
    # agregar el mensaje en formato HTML
    msg.attach(MIMEText(body_html, 'html'))
    
    try:
        # conectar al servidor SMTP de Gmail
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls() # asegura la conexion
            server.login(email_sender, email_password)
            server.sendmail(email_sender, recipient_email, msg.as_string())
            
        return True
    except Exception as e:
        return False, str(e)
# endopoint para enviar el correo
@app.route('/send-email', methods=['POST'])
def send_email_endpoint():
    data = request.json
    subject = data.get('subject')
    recipient = data.get('recipient')
    body_html = data.get('body_html')
    
    success = send_email(subject, recipient, body_html)
    print(f'Success: {success}')
    if success:
        print('Email sent successfully')
        return jsonify({'message': 'Email sent successfully'})
    else:
        print('Error sending email')
        return jsonify({'message': 'Error sending email'})
    
if __name__ == '__main__':
    app.run(debug=True)
    