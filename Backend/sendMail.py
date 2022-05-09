import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ssl import create_default_context


class SendMail:
    def __init__(self):
        try:
            self.sender = "abc@gmail.com"  # Configure a mail id
            self.senderPassword = "password_Of_abc@gmail.com"  # Configure the password of specified mail id
            self.server = smtplib.SMTP("smtp.gmail.com", port=587)
            self.server.connect("smtp.gmail.com", 587)
            self.server.starttls(context=create_default_context())
            self.server.ehlo()
            self.server.login(str(self.sender), str(self.senderPassword))
        except smtplib.SMTPException as e:
            print(e)

    def send(self, receiver, subject, message):
        try:
            msg2 = f'Subject: {subject}\n\n{message}'
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = str(receiver)
            msg['Subject'] = str(subject)
            msg.attach(MIMEText(str(message), 'plain'))
            text = msg.as_string()
            mes = self.server.sendmail(str(self.sender), str(receiver), msg2)
            self.server.close()
        except smtplib.SMTPException as e:
            print(e)
        return
