
with open("bite.html","r") as myfile:
    email_body=myfile.read()

print(email_body)
me  = 'indeed.data@gmail.com'
recipient = 'arnaud.chase@gmail.com'
subject = 'Indeed Report'

email_server_host = 'smtp.gmail.com'
port = 587
email_username = me
email_password = 'indeed123data'

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

msg = MIMEMultipart('alternative')
msg['From'] = me
msg['To'] = recipient
msg['Subject'] = subject

msg.attach(MIMEText(email_body, 'html'))


server = smtplib.SMTP(email_server_host, port)
server.ehlo()
server.starttls()
server.login(email_username, email_password)
server.sendmail(me, recipient, msg.as_string())
server.close()