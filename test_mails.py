import smtplib, ssl
import getpass as gp

port = 465  # For SSL
password = 'indeed123data'

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("indeed.data@gmail.com", password)
    server.sendmail('indeed.data@gmail.com','agbo.arnaud@yahoo.fr','coucou\n')