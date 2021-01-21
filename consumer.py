from kafka import KafkaConsumer
from kafka.errors import KafkaError
from tkinter import *
import tkinter.ttk
from time import sleep
import json
import requests
import msgpack
from requests.exceptions import HTTPError

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('test2',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))

window = Tk()
window.title("My Application")
window.geometry("100x100")
window.minsize(100, 100)
frame = Frame(window, bg = color_background)

def screen(crypto, value):
    etiquette = Label(frame, text=crypto, font=("Courrier", 10), fg = 'black')
    etiquette.pack()
    etiquette2 = Label(frame, text=str(value), font=("Courrier", 10), fg = 'black')
    etiquette2.pack()


for msg in consumer:
    #print(msg.topic + " : ", msg.value)
    screen(msg.topic, msg.value)


consumer.close()
