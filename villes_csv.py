import pandas as pd 
me  = 'indeed.data@gmail.com'
recipient = 'darthmaul9@gmail.com'
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

email_body = """ 
<html>
    <head>
        <meta charset='utf-8'/>
    </head>
    <body>
        <h1>BITE</h1
    </body>
</html>

"""

msg.attach(MIMEText(email_body, 'html'))


    server = smtplib.SMTP(email_server_host, port)
    server.ehlo()
    server.starttls()
    server.login(email_username, email_password)
    server.sendmail(me, recipient, msg.as_string())
    server.close()