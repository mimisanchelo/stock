import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

load_dotenv()

sender = os.getenv('SENDER')
password = os.getenv('EPASSWORD')

headers = {
        "X-RapidAPI-Key": os.getenv('X-API-KEY'),
        "X-RapidAPI-Host": os.getenv('X-API-HOST')}

def send_alert(receiver, ticker, message):
        receiver = receiver

        em = EmailMessage()
        em['From'] = sender
        em['To'] = receiver
        em['Subject'] = f'Alert! There is changes on "{ticker}"'

        content = message
        em.set_content(content)
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, receiver, em.as_string())
