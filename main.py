import requests
from bs4 import BeautifulSoup
import smtplib
from decouple import config

sender_email = config('EMAIL_HOST_USER')
receiver_email = "smitk85143@gmail.com"
password = config('EMAIL_HOST_PASSWORD')

URL = "https://opensea.io/assets/matic/0xdbc52cd5b8eda1a7bcbabb838ca927d23e3673e5/24521426744787990802680776226475879477549827628158815682"
target_price = 11

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
r = requests.get(URL, headers=headers) 

soup = BeautifulSoup(r.content, 'html5lib')

nft_name = soup.find('h1', attrs = {'class':'item--title'}).text
price = float(soup.find('div', attrs = {'class':'Price--fiat-amount'}).text.split("$")[1])

if price <= target_price:
    message = f"""\
    Subject: OpenSea Price Alert of {nft_name}

    {nft_name} is now available at {price} USD. 
    Buy now at {URL}"""
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(from_addr=sender_email, to_addrs=receiver_email, msg=message)
        connection.close()