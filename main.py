import requests
import re
import telebot
from bs4 import BeautifulSoup
from time import sleep

urlglobal = "https://www.kabum.com.br/produto/373931/notebook-gamer-lenovo-gaming-3i-intel-core-i5-11300h-geforce-gtx-1650-8gb-ram-ssd-512gb-15-6-full-hd-windows-11-preto-82mg0009br"
last_price = 5000
interval = 3

#configs do telegram bot
token = "seutoken"
chat_id = seuchatid

def send_message(price):
    global last_price, urlglobal, token, chat_id
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': f'O preço abaixou de R$ {last_price} para R$ {price}. link: {urlglobal}'
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Notificação enviada com sucesso!")
    else:
        print(f"Erro ao enviar notificação. Código de status: {response.status_code}")

def routine():
    global last_price
    while True:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
        }

        url = "https://www.kabum.com.br/produto/373931/notebook-gamer-lenovo-gaming-3i-intel-core-i5-11300h-geforce-gtx-1650-8gb-ram-ssd-512gb-15-6-full-hd-windows-11-preto-82mg0009br"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer a requisição HTTP: {e}")
            sleep(60 * 60 * interval)
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        price_element = soup.find(class_="finalPrice")

        price_content = price_element.string
        real, cents = map(lambda value: re.sub(r'[^0-9]', '', value), price_content.split(','))
        price = float('.'.join([real, cents]))

        if last_price and price < last_price:
                send_message(price)
        last_price = price

        print(last_price)

        sleep(60 * 60 * interval)

routine()
