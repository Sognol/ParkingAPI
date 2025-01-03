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

                if message.is_multipart():
                    for part in message.walk():
                        if part.get_content_type() == "text/plain":
                            email_body = part.get_payload(decode=True).decode()
                            return {"subject": subject, "body": email_body}
                        elif part.get_content_type() == "text/html":
                            email_body = part.get_payload(decode=True).decode()
                            return {"subject": subject, "body": email_body}
                else:
                    email_body = message.get_payload(decode=True).decode()
                    return {"subject": subject, "body": email_body}
    else:
        print("No hay correos nuevos.")
        return None

def main():
    try:
        connection = connect_gmail(USER, PASSWORD)
        result = read_last_mail(connection)
        if result:
            print(f"Asunto: {result['subject']}")
            print(f"Cuerpo: {result['body']}")
    finally:
        connection.logout()

if __name__ == "__main__":
    main()
