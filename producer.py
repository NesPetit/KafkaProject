from kafka import KafkaProducer
from kafka.errors import KafkaError
from tkinter import *
import tkinter.ttk
# from time import sleep
import time
import json
import requests
import msgpack
from requests.exceptions import HTTPError



# Collector API 
dataPriceCoin = 'https://api.coingecko.com/api/v3/simple/price?ids='
dataPriceMarket = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
dataExchange = 'https://api.coingecko.com/api/v3/exchanges/'
dataDeFi = 'https://api.coingecko.com/api/v3/global/decentralized_finance_defi'
dataCoin = 'https://api.coingecko.com/api/v3/coins/'
priceVersus = '&vs_currencies='

listCoin = ['bitcoin', 'ethereum', 'polkadot', 'link', 'havven', 'cardano']

# encode objects via msgpack
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))

while True:
    try:
        print("Start : %s\n" % time.ctime())
        for data in listCoin:
            print("Loading of data")
            response = requests.get(dataCoin + data)
            json_res = response.json()['market_data']['current_price']
            producer.send('cryptot', json_res)
            print(json_res['id'])
            time.sleep(2)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('\nSuccess!\n')

    print("End : %s\n" % time.ctime())

producer.flush()