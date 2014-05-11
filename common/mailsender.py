
import smtplib
from email.mime.text import MIMEText


class MailSender:

    def __init__(self, smtp_host = "localhost"):
        self.smtp_host = smtp_host

    def send(self, subject, sender, to, body):
        """ Call the real sending fucntion as a Thread
        """
        # TODO !
        print("Email sending disabled !")
        pass

    def send_in_background(self, subject, sender, to, body):
        # Prepare the email
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to
 
        # send it
        s = smtplib.SMTP(self.smtp_host)
        s.sendmail(sender, [to], msg.as_string())
        s.quit()


if __name__ == "__main__":
    m = MailSender("smtp.free.fr")
    m.send("sujet", "someone@gmail.com", "someone.else@free.fr", "coucou\nceci est mon mail")
