import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os

EMAIL_ADDRESS = os.environ.get("DEVMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("DEVMAIL_PASSWORD")
# specify the webaddress of the product that you are trying to keep track
URL = 'https://----'


def check_price():
    # specify the webaddress of the product that you are trying to keep track
    URL1 = URL
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id='productTitle').get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    price_1 = price[2:len(price)]
    converted_price = float(price_1.replace(',', ''))
    print(title.strip())
    print(converted_price)

    if(converted_price < 200000):
        send_email()


def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    subject = 'Hey, the price fell down!'
    body = f'Check you amazon link- {URL}'
    msg = f"Subject : {subject}\n\n{body}"
    server.sendmail(
        EMAIL_ADDRESS, EMAIL_ADDRESS, msg
    )
    print('Hey Email Has Been Sent')
    server.quit()


while(True):
    check_price()
    time.sleep(60*60)
