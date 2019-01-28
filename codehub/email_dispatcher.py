import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
#from codehub.config import get_config

config_data = {
    "email_sender" : "codehub.sender@gmail.com",
    "email_sender_password" : "pythoncjs",
    "default" : None,
}
def get_config(key="default"):
    return config_data.get(key,None)


def send_mail(send_from, send_to, subject, text, files=None,
              server='smtp.gmail.com', port=587):
    #assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP(server, port)
    smtp.starttls()
    smtp.login(get_config("email_sender"), password="pythonc++")
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

send_mail(get_config("email_sender"),"15pa1a05e0@vishnu.edu.in",subject= "Test Email" ,text ="THis is a test Mail" )