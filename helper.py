import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
import pip._vendor.requests as request

load_dotenv()

sender = os.getenv('SENDER')
password = os.getenv('EPASSWORD')

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

headers = {
        "X-RapidAPI-Key": os.getenv('X-API-KEY'),
        "X-RapidAPI-Host": os.getenv('X-API-HOST')}

def get_quote_symbol(symbol):
        url = "https://twelve-data1.p.rapidapi.com/quote"
        querystring = {"symbol":symbol,"interval":"1day","outputsize":"30","format":"json"}
        response_ticker = request.get(url, headers=headers, params=querystring).json()
        return response_ticker

def get_price_symbol(symbol):
        url_price = "https://twelve-data1.p.rapidapi.com/price"
        query = {"symbol":symbol,"format":"json","outputsize":"30"}
        response_price = request.get(url_price, headers=headers, params=query).json()
        return response_price

def get_profile_symbol(symbol):
        url_profile = "https://twelve-data1.p.rapidapi.com/profile"
        querystring = {"symbol":symbol}
        response_profile = request.get(url_profile, headers=headers, params=querystring).json()
        return response_profile