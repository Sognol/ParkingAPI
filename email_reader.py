import imaplib
import email
from email.header import decode_header
from decouple import config

USER = config("EMAIL_USER")
PASSWORD = config("PASSWORD")

def connect_gmail(user, password):
    server = "imap.gmail.com"
    connection = imaplib.IMAP4_SSL(server)
    connection.login(user, password)
    return connection

def read_last_mail(connection):
    connection.select("inbox")
    
    status, messages = connection.search(None, "UNSEEN")
    
    if messages[0]:
        last_mail = messages[0].split()[-1]
        status, data = connection.fetch(last_mail, "(RFC822)")
        
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])

                subject, encoding = decode_header(message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                print(f"Asunto:", subject)
                
                if message.is_multipart():
                    for part in message.walk():
                        if part.get_content_type() == "text/plain":
                            email_body = part.get_payload(decode=True).decode()
                            print(f"Cuerpo:\n{email_body}")
                            return email_body
                else:
                    email_body = message.get_payload(decode=True).decode()
                    print(f"Cuerpo:\n{email_body}")
                    return email_body
                
    else:
        print("No hay correos nuevos.")
        return None
    
try:
    connection = connect_gmail(USER, PASSWORD)
    email_body = read_last_mail(connection)
    if email_body:
        print("Correo leído correctamente.")
        connection.logout()
except Exception as e:
    print(f"Error al leer el correo: {e}")
        