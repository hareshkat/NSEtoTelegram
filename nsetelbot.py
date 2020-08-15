from telbot import telegram_chatbot
from datetime import datetime
from nsetools import Nse
import time
import requests
from bs4 import BeautifulSoup


nse = Nse()
bot = telegram_chatbot("config.cfg")
tel_chat_ids = [634768894, 504002672]
previousPrice = 0

def isAlert(currentStrikePrice, previousStrikePrice, timestamp=datetime.now().strftime("%H:%M:%S")):
    if (abs(float(currentStrikePrice) - float(previousStrikePrice)) >= 10):
        for chat_id in tel_chat_ids:
            reply = 'Nifty Bank : {} ({})'.format(currentStrikePrice, timestamp)
            bot.send_message(reply, chat_id)
        print("ALERT")


# def fetchPrice(symbol):
#     global previousPrice
#     data = nse.get_index_quote(symbol)  
#     currentStrikePrice = data['lastPrice']
#     isAlert(currentStrikePrice,previousPrice)
#     print("Time = "+ datetime.now().strftime("%H:%M:%S") +" | Current Price : "+ str(currentStrikePrice) +" | Previous Price : "+ str(previousPrice) )
#     previousPrice = currentStrikePrice
#     time.sleep(60)

def fetchPrice(symbol):
    global previousPrice
    url = 'https://in.investing.com/indices/bank-nifty'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'xml')
        price = soup.find_all(class_="last-price-value js-streamable-element")
        if price:
            currentStrikePrice = float(price[0].text.replace(',',''))
        timestamp = soup.find_all(class_="inbetween-time")[0].time.text
    except:
        currentStrikePrice = 0
        timestamp = '00:00:00'
    if(previousPrice != 0 and currentStrikePrice != 0):
        isAlert(currentStrikePrice,previousPrice, timestamp)
    print("Time = "+ timestamp +" | Current Price : "+ str(currentStrikePrice) +" | Previous Price : "+ str(previousPrice) )
    previousPrice = currentStrikePrice
    time.sleep(10)


def main():
    symbol = "nifty bank"
    while True:
        fetchPrice(symbol)


if __name__ == '__main__':
    main()